from django.urls import path,include
from user.views import UserAPIView,CreateTokenView


urlpatterns = [
    path('users/', UserAPIView.as_view()),  # For GET and POST requests
    path('users/<int:pk>/', UserAPIView.as_view()),
    path('token/',CreateTokenView.as_view()),
]