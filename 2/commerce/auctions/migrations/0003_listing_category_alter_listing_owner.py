# Generated by Django 5.0.2 on 2024-03-24 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
