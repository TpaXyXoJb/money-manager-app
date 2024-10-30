from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

from ..models.category import Category
from ..serializers.category import CategorySerializer
from ..filters.category import CategoryFilter
from ..permissions import IsOwner


class CategoryViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      ListModelMixin,
                      GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        queryset = Category.objects.all()
        if self.action == 'get_all_categories_info':
            self.filter_backends = (DjangoFilterBackend,)
            self.filterset_class = CategoryFilter
            queryset = self.filter_queryset(
                queryset.annotate(
                    amount=Coalesce(
                        Sum('transaction__amount'),
                        Value(0),
                        output_field=DecimalField()
                    )
                )
            )
        return queryset

    @action(detail=False, methods=['GET'])
    def get_all_categories_info(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=HTTP_200_OK)
