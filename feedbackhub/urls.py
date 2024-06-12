from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, CompanyViewSet, CategoryViewSet, FeedbackViewSet, NotificationViewSet, MyTokenObtainPairView, RegisterUser, MetricsViewSet

urlpatterns = [
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('companies/', CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
    path('companies/<int:pk>/', CompanyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='company-detail'),
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('metrics/', MetricsViewSet.as_view({'get': 'list', }), name='metric-list'),

    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('feedbacks/', FeedbackViewSet.as_view({'get': 'list', 'post': 'create'}), name='feedback-list'),
    path('feedbacks/<int:pk>/', FeedbackViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='feedback-detail'),
    path('notifications/', NotificationViewSet.as_view({'get': 'list', 'post': 'create'}), name='notification-list'),
    path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='notification-detail'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]
