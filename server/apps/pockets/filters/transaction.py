from django_filters.rest_framework import FilterSet, DateFilter

from ..models.transaction import Transaction


class TransactionFilter(FilterSet):
    date = DateFilter(field_name='date', label='Date')
    start_date = DateFilter(field_name='date', lookup_expr='gte',label='From')
    end_date = DateFilter(field_name='date', lookup_expr='lte', label='To')

    class Meta:
        model = Transaction
        fields = ('date', 'start_date', 'end_date')
