from django_filters.rest_framework import FilterSet, DateFilter

from ..models.category import Category


class CategoryFilter(FilterSet):
    date = DateFilter(field_name='transaction__date')
    start_date = DateFilter(field_name='transaction__date', lookup_expr='gte')
    end_date = DateFilter(field_name='transaction__date', lookup_expr='lte')

    class Meta:
        model = Category
        fields = ('date', 'start_date', 'end_date')
