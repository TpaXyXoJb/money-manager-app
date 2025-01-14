# Generated by Django 3.2.2 on 2024-10-29 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pockets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='date'),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='sum limit')),
                ('duration', models.DurationField(verbose_name='duration')),
                ('criterion', models.CharField(choices=[('>', 'Greater than'), ('<', 'Less than')], max_length=2, verbose_name='criterion')),
                ('colour', models.CharField(default='#000000', max_length=7, verbose_name='colour HEX')),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='pockets.category', verbose_name='category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
            },
        ),
    ]
