# Generated by Django 3.2.25 on 2024-11-09 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_book_publishers'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='book',
            field=models.ManyToManyField(related_name='books', to='catalog.Book'),
        ),
    ]
