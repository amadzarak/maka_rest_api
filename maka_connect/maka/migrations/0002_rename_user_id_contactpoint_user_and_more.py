# Generated by Django 5.0.3 on 2024-03-11 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactpoint',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='conversationstarters',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]
