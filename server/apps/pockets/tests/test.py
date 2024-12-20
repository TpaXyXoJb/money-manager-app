import pytest
from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.tests.factories import UserFactory
from .factories import CategoryFactory, TransactionFactory, WidgetFactory
from ..models.category import Category
from ..models.transaction import Transaction
from ..models.widget import Widget


@pytest.fixture
def authenticated_client():
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    client.user = user
    return client


@pytest.mark.django_db
def test_create_category_authenticated(authenticated_client):
    """
    Test creating a category as an authenticated user
    """
    data = {
        'name': 'test category',
        'category_type': 'IN'
    }
    response = authenticated_client.post(reverse('category-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data['name'] == 'test category'
    assert response.data['category_type'] == 'IN'
    assert response.data['owner'] == authenticated_client.user.id
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_create_category_unauthenticated():
    """
    Test that an unauthenticated user cannot create a category
    """
    unauthenticated_client = APIClient()

    data = {
        'name': 'test category',
        'category_type': 'IN'
    }
    response = unauthenticated_client.post(reverse('category-list'), data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_category_list(authenticated_client):
    """
    Test retrieving a list of categories for authenticated user
    """
    CategoryFactory.create_batch(3, owner=authenticated_client.user)
    response = authenticated_client.get(reverse('category-list'))
    assert response.status_code == status.HTTP_200_OK
    assert Category.objects.count() == 3


@pytest.mark.django_db
def test_category_delete_only_owner(authenticated_client):
    """
    Test deleting a category by its owner
    """
    category = CategoryFactory(owner=authenticated_client.user)
    other_user_category = CategoryFactory()
    unauthenticated_client = APIClient()

    response = authenticated_client.delete(reverse('category-detail', args=[category.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Category.objects.filter(id=category.id).exists()

    response = authenticated_client.delete(reverse('category-detail', args=[other_user_category.id]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not Category.objects.filter(id=category.id).exists()

    response = unauthenticated_client.delete(reverse('category-detail', args=[category.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not Category.objects.filter(id=category.id).exists()


@pytest.mark.django_db
def test_get_all_categories_info(authenticated_client):
    """
    Test retrieving all categories with aggregated transaction amounts
    """
    category1 = CategoryFactory(owner=authenticated_client.user)
    category2 = CategoryFactory(owner=authenticated_client.user)
    TransactionFactory.create_batch(3, category=category1, amount=100)
    TransactionFactory.create_batch(2, category=category2, amount=30)

    response = authenticated_client.get(reverse('category-get-all-categories-info'))

    assert response.status_code == status.HTTP_200_OK

    amounts = {item['id']: item['amount'] for item in response.data}
    assert amounts[category1.id] == '300.00'
    assert amounts[category2.id] == '60.00'


@pytest.mark.django_db
def test_get_all_categories_info_unauthenticated():
    """
    Test that unauthenticated users have no access to get all categories info
    :return:
    """
    unauthenticated_client = APIClient()

    response = unauthenticated_client.get(reverse('category-get-all-categories-info'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_transaction_authenticated(authenticated_client):
    """
    Test creating a transaction as an authenticated user
    """
    category = CategoryFactory(owner=authenticated_client.user, category_type='EXP')

    data = {
        'amount': 300.00,
        'category': category.id
    }

    response = authenticated_client.post(reverse('transaction-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data['amount'] == '300.00'
    assert response.data['category'] == category.id
    assert response.data['owner'] == authenticated_client.user.id
    assert Transaction.objects.count() == 1


@pytest.mark.django_db
def test_create_transaction_unauthenticated():
    """
    Test that an unauthenticated user cannot create a transaction
    """
    unauthenticated_client = APIClient()

    category = CategoryFactory()

    data = {
        'amount': 300.00,
        'category': category.id
    }
    response = unauthenticated_client.post(reverse('transaction-list'), data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_transaction_list_authenticated(authenticated_client):
    """
    Test retrieving a list of transactions for authenticated user
    """
    TransactionFactory.create_batch(3, owner=authenticated_client.user)
    TransactionFactory.create_batch(2)

    response = authenticated_client.get(reverse('transaction-list'))

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data['results']) == 3
    for transaction in response.data['results']:
        assert transaction['owner'] == authenticated_client.user.id


@pytest.mark.django_db
def test_transaction_list_unauthenticated():
    """
    Test that unauthenticated user cannot get access for a list of transactions
    """
    TransactionFactory.create_batch(3)

    unauthenticated_client = APIClient()

    response = unauthenticated_client.get(reverse('transaction-list'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'results' not in response.data


@pytest.mark.django_db
def test_transaction_list_filter_by_category(authenticated_client):
    """
    Test case for filtering transactions by category
    """
    category = CategoryFactory(owner=authenticated_client.user)
    TransactionFactory.create_batch(2, owner=authenticated_client.user, category=category)
    TransactionFactory.create_batch(3, owner=authenticated_client.user)

    response = authenticated_client.get(reverse('transaction-list'), {'category': category.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    for transaction in response.data['results']:
        assert transaction['category'] == category.id


@pytest.mark.django_db
def test_transaction_list_pagination(authenticated_client):
    """
    Test validating pagination in the transaction list endpoint
    """
    TransactionFactory.create_batch(50, owner=authenticated_client.user)

    response = authenticated_client.get(reverse('transaction-list'), {'page': 1})
    response_page_2 = authenticated_client.get(reverse('transaction-list'), {'page': 2})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) <= 20
    assert response_page_2.status_code == status.HTTP_200_OK
    assert len(response_page_2.data['results']) <= 20


@pytest.mark.django_db
def test_transaction_delete_only_owner(authenticated_client):
    """
    Test deleting a transaction by its owner
    """
    transaction = TransactionFactory(owner=authenticated_client.user)
    other_user_transaction = TransactionFactory()
    unauthenticated_client = APIClient()

    response = authenticated_client.delete(reverse('transaction-detail', args=[transaction.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Transaction.objects.filter(id=transaction.id).exists()

    response = authenticated_client.delete(reverse('transaction-detail', args=[other_user_transaction.id]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not Transaction.objects.filter(id=transaction.id).exists()

    response = unauthenticated_client.delete(reverse('transaction-detail', args=[transaction.id]))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not Transaction.objects.filter(id=transaction.id).exists()


@pytest.mark.django_db
def test_transaction_update_only_owner(authenticated_client):
    """
    Test updating a transaction by its owner
    """
    transaction = TransactionFactory(owner=authenticated_client.user)
    other_user_transaction = TransactionFactory()
    unauthenticated_client = APIClient()

    data = {
        'amount': 333.00,
        'category': transaction.category.id
    }

    response = authenticated_client.put(reverse('transaction-detail', args=[transaction.id]), data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['amount'] == '333.00'

    response = authenticated_client.put(reverse('transaction-detail', args=[other_user_transaction.id]), data)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = unauthenticated_client.put(reverse('transaction-detail', args=[transaction.id]), data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_global_info_action(authenticated_client):
    """
    Test retrieving global income and expense summaries
    """
    TransactionFactory.create_batch(3, owner=authenticated_client.user, category__category_type='IN', amount=100)
    TransactionFactory.create_batch(2, owner=authenticated_client.user, category__category_type='EXP', amount=50)

    response = authenticated_client.get(reverse('transaction-global-info'))

    assert response.status_code == status.HTTP_200_OK
    assert 'income' in response.data
    assert 'expense' in response.data
    assert response.data['income'] == 300
    assert response.data['expense'] == 100


@pytest.mark.django_db
def test_global_info_action_no_transaction(authenticated_client):
    """
    Test retrieving global income and expense summaries when there are no transactions
    """
    response = authenticated_client.get(reverse('transaction-global-info'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['income'] == 0
    assert response.data['expense'] == 0


@pytest.mark.django_db
def test_global_info_action_other_user_transaction(authenticated_client):
    """
    Test ensuring that transactions from other users are excluded in global info
    """
    TransactionFactory.create_batch(2, owner=authenticated_client.user, category__category_type='IN', amount=100)
    TransactionFactory.create_batch(3, category__category_type='EXP', amount=50)

    response = authenticated_client.get(reverse('transaction-global-info'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data['income'] == 200
    assert response.data['expense'] == 0


@pytest.mark.django_db
def test_create_widget_authenticated(authenticated_client):
    """
    Test creating a widget as an authenticated user
    """
    category = CategoryFactory(owner=authenticated_client.user)
    data = {
        'category': category.id,
        'limit': 1000.00,
        'duration': timedelta(days=30),
        'criterion': '>',
        'colour': '#FF5733'
    }
    response = authenticated_client.post(reverse('widget-list'), data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data['limit'] == '1000.00'
    assert response.data['category'] == category.id
    assert response.data['owner'] == authenticated_client.user.id
    assert response.data['criterion'] == '>'
    assert response.data['colour'] == '#FF5733'

    assert Widget.objects.count() == 1


@pytest.mark.django_db
def test_create_widget_unauthenticated():
    """
    Test that an unauthenticated user cannot create a widget
    """
    category = CategoryFactory()
    data = {
        'category': category.id,
        'limit': 1000.00,
        'duration': timedelta(days=30),
        'criterion': '>',
        'colour': '#FF5733'
    }
    unauthenticated_client = APIClient()

    response = unauthenticated_client.post(reverse('widget-list'), data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Widget.objects.count() == 0


@pytest.mark.django_db
def test_widget_list(authenticated_client):
    """
    Test retrieving a list of widgets for authenticated user
    """
    WidgetFactory.create_batch(3, owner=authenticated_client.user)
    WidgetFactory.create_batch(2)
    response = authenticated_client.get(reverse('widget-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    for widget in response.data:
        assert widget['owner'] == authenticated_client.user.id


@pytest.mark.django_db
def test_widget_delete_only_owner(authenticated_client):
    """
    Test deleting a widget by its owner
    """
    widget = WidgetFactory(owner=authenticated_client.user)
    other_user_widget = WidgetFactory()
    unauthenticated_client = APIClient()

    response = authenticated_client.delete(reverse('widget-detail', args=[widget.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Widget.objects.filter(id=widget.id).exists()

    response = authenticated_client.delete(reverse('widget-detail', args=[other_user_widget.id]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not Widget.objects.filter(id=widget.id).exists()

    response = unauthenticated_client.delete(reverse('widget-detail', args=[widget.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not Widget.objects.filter(id=widget.id).exists()
