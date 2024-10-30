from rest_framework import routers

from .viewsets.category import CategoryViewSet
from .viewsets.transaction import TransactionViewSet
from .viewsets.widget import WidgetViewSet

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'transaction', TransactionViewSet, basename='transaction')
router.register(r'widget', WidgetViewSet, basename='widget')
