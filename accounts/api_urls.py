from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import RegisterAPIView, LoginAPIView, MeAPIView

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeAPIView.as_view(), name='api_me'),
]


