from django_filters.rest_framework import FilterSet, DateFilter

from ..models.category import Category


class CategoryFilter(FilterSet):
    """
    Category filter
    """
    date = DateFilter(field_name='transaction__date', label='Date')
    start_date = DateFilter(field_name='transaction__date', lookup_expr='gte', label='From')
    end_date = DateFilter(field_name='transaction__date', lookup_expr='lte', label='To')

    class Meta:
        model = Category
        fields = ('date', 'start_date', 'end_date')
