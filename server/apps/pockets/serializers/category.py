from rest_framework import serializers, fields

from ..models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the category model
    """
    amount = fields.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'owner', 'category_type', 'amount')
        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        category = Category.objects.create(**validated_data)
        category.save()
        return category
