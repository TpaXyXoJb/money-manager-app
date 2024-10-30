from ..models.widget import Widget

from rest_framework import serializers


class WidgetSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    duration = serializers.DurationField()
    end_date = serializers.SerializerMethodField()

    def get_end_date(self, obj):
        return obj.created + obj.duration

    class Meta:
        model = Widget
        fields = (
            'id',
            'owner',
            'category',
            'limit',
            'duration',
            'criterion',
            'colour',
            'created',
            'end_date',
            'amount',
        )