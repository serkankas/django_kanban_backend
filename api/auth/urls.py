from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.urls import path
from . import views

urlpatterns = [
    path('/token/get/', views.CustomizedTokenObtainPairView.as_view(), name='get_token'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
