from django_filters.rest_framework import FilterSet, DateFilter, NumberFilter

from ..models.transaction import Transaction


class TransactionFilter(FilterSet):
    """
    Transaction filter
    """
    date = DateFilter(field_name='date', label='Date')
    start_date = DateFilter(field_name='date', lookup_expr='gte', label='From')
    end_date = DateFilter(field_name='date', lookup_expr='lte', label='To')
    category = NumberFilter(field_name='category_id', label='Category ID')

    class Meta:
        model = Transaction
        fields = ('date', 'start_date', 'end_date', 'category')
