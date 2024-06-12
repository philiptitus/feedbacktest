from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import CustomUser, Company, Category, Feedback, Notification
from .serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
       def validate(self, attrs: dict[str, any]) -> dict[str, str]:
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        

        return data
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import CustomUser
from .serializers import CustomUserSerializer
from .utils import send_normal_email  # Assuming you have a utility function to send emails

class RegisterUser(APIView):

    def post(self, request):
        data = request.data

        print("Data received from the form:", data)

        # Check if user type is provided
        user_type = data.get('user_type')
        if user_type not in ['admin', 'normal_user']:
            return Response({'detail': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

        # Define required fields based on user type
        fields_to_check = ['first_name', 'last_name', 'email', 'password']

        # Check if all required fields are present
        for field in fields_to_check:
            if field not in data:
                return Response({'detail': f'Missing {field} field.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check password length
        if len(data['password']) < 8:
            content = {'detail': 'Password must be at least 8 characters long.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Check password for username and email
        if data['password'].lower() in [data['first_name'].lower(), data['email'].lower()]:
            content = {'detail': 'Password cannot contain username or email.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        try:
            validate_email(data['email'])
        except ValidationError:
            return Response({'detail': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password strength
        try:
            validate_password(data['password'])
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            user = CustomUser.objects.create_user(
                username=data['email'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
                is_admin=(user_type == 'admin'),
                is_normal_user=(user_type == 'normal_user')
            )

            email_subject = "Welcome to FeedbackHub"
            email_message = "Hello {},\n\nWelcome to FeedbackHub! Your account has been created successfully.".format(user.first_name)
            to_email = user.email
            email_data = {
                'email_body': email_message,
                'email_subject': email_subject,
                'to_email': to_email
            }
            send_normal_email(email_data)
        except IntegrityError:
            message = {'detail': 'User with this email already exists.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework import viewsets, permissions, status



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow company admins to edit or delete company instances.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the company admin
        return obj.administrator == request.user

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyAdminOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the administrator field to the request user
        serializer.save(administrator=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Feedback
from .serializers import FeedbackSerializer
from .utils import send_normal_email  # Import the utility function for sending emails

class IsCompanyAdminToUpdate(permissions.BasePermission):
    """
    Custom permission to only allow company admins to update feedback instances.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the company admin
        return obj.company.administrator == request.user

class IsNormalUserToCreate(permissions.BasePermission):
    """
    Custom permission to only allow normal users to create feedback instances.
    """
    def has_permission(self, request, view):
        # Write permissions are only allowed to normal users
        return request.user.is_normal_user

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feedback, Notification
from .serializers import FeedbackSerializer
from .utils import send_normal_email

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Feedback, Notification
from .serializers import FeedbackSerializer
from .utils import send_normal_email

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_normal_user:
            # Return feedbacks created by the normal user
            return Feedback.objects.filter(user=user)

        if user.is_admin:
            # Get feedbacks for the company where the user is an admin and mark them as read
            feedbacks = Feedback.objects.filter(company__administrator=user)
            return feedbacks

        # By default return an empty queryset (or handle other user roles if any)
        return Feedback.objects.none()

    def perform_create(self, serializer):
        feedback = serializer.save(user=self.request.user)
        admin_email = feedback.company.administrator.email
        subject = "New Feedback Submission"
        message = f"A new feedback has been submitted. Title: {feedback.title}"
        send_normal_email({'email_body': message, 'email_subject': subject, 'to_email': admin_email})

        Notification.objects.create(
            feedback=feedback,
            user=feedback.company.administrator,
            message=message
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        allowed_fields = ['status']
        if not all(field in request.data.keys() for field in allowed_fields):
            return Response({'detail': 'You can only update the status field.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()

            # Notify the user who created the feedback
            user_email = instance.user.email
            subject = "Feedback Status Updated"
            user_message = f"The status of your feedback '{instance.title}' has been updated to {instance.status}."
            send_normal_email({'email_body': user_message, 'email_subject': subject, 'to_email': user_email})

            Notification.objects.create(
                feedback=instance,
                user=instance.user,
                message=user_message
            )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        admin_email = instance.company.administrator.email
        subject = "Feedback Deleted"
        message = f"The feedback '{instance.title}' has been deleted."
        send_normal_email({'email_body': message, 'email_subject': subject, 'to_email': admin_email})

        Notification.objects.create(
            feedback=instance,
            user=instance.company.administrator,
            message=message
        )

        instance.delete()

from rest_framework import viewsets, permissions
from .models import Notification, Metrics, Feedback, Company
from .serializers import NotificationSerializer, MetricsSerializer
from django.db.models import Avg, Count

from rest_framework import viewsets, permissions
from .models import Notification, Metrics, Feedback, Company
from .serializers import NotificationSerializer, MetricsSerializer
from django.db.models import Avg, Count

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin and user.has_company:
            company = Company.objects.get(administrator=user)
            feedbacks = Feedback.objects.filter(company=company)

            if feedbacks.count() > 5:
                categories = feedbacks.values('category__name').annotate(avg_rating=Avg('rating')).filter(avg_rating__isnull=False)

                if categories:
                    best_category = max(categories, key=lambda x: x['avg_rating'])
                    worst_category = min(categories, key=lambda x: x['avg_rating'])

                    if best_category['category__name'] != worst_category['category__name']:
                        best_description = f'Your best performing aspect was {best_category["category__name"]} with an average rating of {best_category["avg_rating"]}.'
                        worst_description = f'Your worst performing aspect was {worst_category["category__name"]} with an average rating of {worst_category["avg_rating"]}.'

                        Metrics.objects.get_or_create(company=company, description=best_description)
                        Metrics.objects.get_or_create(company=company, description=worst_description)

                total_feedbacks = feedbacks.count()
                feedbacks_description = f'Your total feedbacks are currently {total_feedbacks}.'
                Metrics.objects.get_or_create(company=company, description=feedbacks_description)

                avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
                avg_rating_description = f'Your average website rating is {avg_rating}.'
                Metrics.objects.get_or_create(company=company, description=avg_rating_description)

                sentiment = 'happy' if avg_rating >= 3 else 'sad'
                sentiment_description = f'Most people are {sentiment} with your website based on the average rating of {avg_rating}.'
                Metrics.objects.get_or_create(company=company, description=sentiment_description)

        return Notification.objects.filter(user=self.request.user)

class MetricsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin and user.has_company:
            company = Company.objects.get(administrator=user)
            return Metrics.objects.filter(company=company)
        return Metrics.objects.none()
