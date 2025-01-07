import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for User
    """
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    username = factory.Faker('user_name')
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.PostGenerationMethodCall('set_password', 'testuserpassword123')
