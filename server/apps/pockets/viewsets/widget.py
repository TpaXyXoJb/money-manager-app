from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)

from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema

from ..models.widget import Widget
from ..serializers.widget import WidgetSerializer
from ..permissions import IsOwner
from .swagger_docs import swagger_widget_viewset


@swagger_auto_schema(**swagger_widget_viewset)
class WidgetViewSet(CreateModelMixin,
                    DestroyModelMixin,
                    ListModelMixin,
                    GenericViewSet):
    """
    Widget viewset
    """
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        queryset = Widget.objects.filter(owner=self.request.user)
        if self.action == 'list':
            queryset = queryset.annotate(
                amount=Coalesce(
                    Sum('category__transaction__amount'),
                    Value(0),
                    output_field=DecimalField()
                )
            )
        return queryset
