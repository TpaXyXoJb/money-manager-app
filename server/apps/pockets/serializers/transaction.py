from rest_framework import serializers, fields

from ..models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    category_type = fields.CharField(source='category.category_type', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'owner', 'category', 'amount', 'date', 'category_type')
