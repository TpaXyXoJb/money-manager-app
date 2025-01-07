from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import User
from ..serializers import UserSummarySerializer


class UserSummaryAPIView(generics.RetrieveAPIView):
    """
    User summary view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSummarySerializer

    def get_object(self) -> User:
        return self.request.user
