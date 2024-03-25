# Generated by Django 5.0.2 on 2024-03-25 12:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_item_remove_listing_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlisted_by',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
