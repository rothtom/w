# Generated by Django 5.0.2 on 2024-03-31 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_following_post_user_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to='network.post'),
        ),
    ]