from rest_framework.pagination import PageNumberPagination

PAGE_SIZE = 20
MAX_PAGE_SIZE = 20


class TransactionSetPagination(PageNumberPagination):
    """
    Pagination class for the Transaction
    """
    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE
