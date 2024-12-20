from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import (CreateModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema

from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer
from ..filters.transaction import TransactionFilter
from ..paginators import TransactionSetPagination
from ..permissions import IsOwner
from .swagger_docs import swagger_transaction_viewset, swagger_transaction_global_info


@swagger_auto_schema(**swagger_transaction_viewset)
class TransactionViewSet(CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    serializer_class = TransactionSerializer
    pagination_class = TransactionSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        return self.filter_queryset(Transaction.objects.filter(owner=self.request.user))

    @swagger_auto_schema(**swagger_transaction_global_info)
    @action(detail=False, methods=['GET'])
    def global_info(self, request):
        queryset = self.get_queryset().aggregate(
            income=Coalesce(
                Sum(
                    'amount',
                    filter=Q(category__category_type='IN'),
                ),
                Value(0),
                output_field=DecimalField()
            ),
            expense=Coalesce(
                Sum(
                    'amount',
                    filter=Q(category__category_type='EXP'),
                ),
                Value(0),
                output_field=DecimalField()
            )
        )
        return Response(queryset, HTTP_200_OK)
