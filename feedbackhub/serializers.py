from rest_framework import serializers
from .models import CustomUser, Company, Category, Feedback, Notification, Metrics



from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import jwt
from pytz import timezone  # Import timezone from pytz
from datetime import timedelta



class CustomUserSerializer(serializers.ModelSerializer):
    has_company = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_has_company(self, obj):
        return obj.has_company

class UserSerializerWithToken(CustomUserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    expiration_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'is_normal_user', 'token', 'expiration_time']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_expiration_time(self, obj):
        token = RefreshToken.for_user(obj)
        access_token = str(token.access_token)
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})  # Decode token without verification
        expiration_timestamp = decoded_token['exp']  # Get the expiration time from the decoded token
        expiration_datetime_utc = datetime.utcfromtimestamp(expiration_timestamp)  # Convert expiration timestamp to UTC datetime
        expiration_datetime_local = expiration_datetime_utc.astimezone(timezone('Africa/Nairobi'))  # Convert to Nairobi timezone
        return expiration_datetime_local.strftime('%Y-%m-%d %H:%M:%S %Z')  # Return as a formatted string




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

from rest_framework import serializers
from .models import Feedback, Category

class FeedbackSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    company_name = serializers.ReadOnlyField(source='company.name')


    class Meta:
        model = Feedback
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'POST':
            # Exclude 'user' field from serializer during creation
            data.pop('user', None)
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics
        fields = '__all__'