# Generated by Django 3.0.4 on 2020-05-05 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20200502_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskanswer',
            name='text',
            field=models.TextField(default='', verbose_name='Сообщение'),
        ),
    ]