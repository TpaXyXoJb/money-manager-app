from rest_framework import serializers, fields

from ..models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    amount = fields.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'owner', 'category_type', 'amount')
