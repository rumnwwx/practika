# Generated by Django 3.2.25 on 2024-11-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_publisher_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishers',
            field=models.ManyToManyField(related_name='book_set', to='catalog.Publisher'),
        ),
    ]