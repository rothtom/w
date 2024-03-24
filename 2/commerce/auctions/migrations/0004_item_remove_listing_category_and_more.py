# Generated by Django 5.0.2 on 2024-03-24 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category_alter_listing_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=48)),
                ('description', models.CharField(max_length=128)),
                ('picture_link', models.URLField(blank=True)),
                ('category', models.CharField(blank=True, max_length=16)),
                ('starting_bid', models.IntegerField(max_length=12)),
            ],
        ),
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='description',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='picture_link',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='title',
        ),
        migrations.AddField(
            model_name='listing',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.item'),
            preserve_default=False,
        ),
    ]
