from rest_framework import serializers, fields

from ..models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """
    category_type = fields.CharField(source='category.category_type', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'owner', 'category', 'amount', 'date', 'category_type')
        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        transaction = Transaction(**validated_data)
        transaction.save()
        return transaction
