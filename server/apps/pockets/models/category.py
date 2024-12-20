from django.db import models


class Category(models.Model):
    """
    Category model
    """
    INCOME = 'IN'
    EXPENSE = 'EXP'
    CATEGORY_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    owner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name='owner',
    )
    category_type = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES,
        verbose_name='category_type',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.pk)
