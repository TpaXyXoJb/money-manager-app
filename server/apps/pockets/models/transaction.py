from django.db import models


class Transaction(models.Model):
    """
    Transaction model
    """
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
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return str(self.amount)
