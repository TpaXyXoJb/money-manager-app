from django.db import models
from datetime import timedelta


class Widget(models.Model):
    GT = '>'
    LT = '<'
    CRITERION_CHOICES = [
        (GT, 'Greater than'),
        (LT, 'Less than'),
    ]
    owner = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name='owner',
    )
    category = models.ForeignKey(
        to='pockets.Category',
        on_delete=models.CASCADE,
        verbose_name='category',
        related_name='widgets',
    )
    limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='sum limit',
    )
    duration = models.DurationField(
        verbose_name='duration',
    )
    criterion = models.CharField(
        max_length=2,
        choices=CRITERION_CHOICES,
        verbose_name='criterion'
    )
    colour = models.CharField(
        max_length=7,
        default='#000000',
        verbose_name='colour HEX',
    )
    created = models.DateField(
        verbose_name='created',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'

    def __str__(self):
        return str(self.pk)
