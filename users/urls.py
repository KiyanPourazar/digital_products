from django.urls import path
from .views import RegisterView, GetToken

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('gettoken/', GetToken.as_view(), name='gettoken'),
]