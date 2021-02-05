# Generated by Django 3.0.4 on 2020-04-24 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0005_auto_20200403_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='registrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registrator', to=settings.AUTH_USER_MODEL, verbose_name='Регистратор'),
        ),
        migrations.AlterField(
            model_name='document',
            name='signer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signer', to=settings.AUTH_USER_MODEL, verbose_name='Подписант'),
        ),
    ]