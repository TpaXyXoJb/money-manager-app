from django.urls import path
from rest_framework.authtoken import views


from ..views import UserCreateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
]
