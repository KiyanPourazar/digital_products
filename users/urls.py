from django.urls import path

from rest_framework_simplejwt.views import (
                                            TokenRefreshView,
                                            TokenObtainPairView,
)

from .views import RegisterView, GetToken


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('gettoken/', GetToken.as_view(), name='gettoken'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]