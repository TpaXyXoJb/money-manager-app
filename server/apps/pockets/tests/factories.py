import factory
import datetime
from factory import fuzzy
from apps.users.tests.factories import UserFactory
from apps.pockets.models.category import Category
from apps.pockets.models.transaction import Transaction
from apps.pockets.models.widget import Widget


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory for Category tests
    """
    class Meta:
        model = Category

    name = fuzzy.FuzzyText()
    owner = factory.SubFactory(UserFactory)
    category_type = fuzzy.FuzzyChoice(['IN', 'EXP'])


class TransactionFactory(factory.django.DjangoModelFactory):
    """
    Factory for Transaction tests
    """
    class Meta:
        model = Transaction

    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = fuzzy.FuzzyDecimal(0.01, 100000.00, 2)
    date = fuzzy.FuzzyDate(datetime.date(2018, 1, 1))


class WidgetFactory(factory.django.DjangoModelFactory):
    """
    Factory for Widget tests
    """
    class Meta:
        model = Widget

    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    limit = fuzzy.FuzzyDecimal(100.00, 100000.00, 2)
    duration = fuzzy.FuzzyChoice((datetime.timedelta(days=i) for i in range(1, 32)))
    criterion = fuzzy.FuzzyChoice((Widget.GT, Widget.LT))
    colour = fuzzy.FuzzyChoice(('#ff0000', '#00ff00', '#0000ff', '#000000', '#ffffff'))
