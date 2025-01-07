from rest_framework import generics

from ..serializers import UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    User create view
    """
    serializer_class = UserCreateSerializer
