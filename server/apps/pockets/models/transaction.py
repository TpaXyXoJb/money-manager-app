from django.db import models
from datetime import date


class Transaction(models.Model):
    owner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name='owner'
    )
    category = models.ForeignKey(
        to='pockets.Category',
        on_delete=models.CASCADE,
        verbose_name='category'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='amount'
    )
    date = models.DateField(
        verbose_name='date',
        default=date.today
    )

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return str(self.amount)
