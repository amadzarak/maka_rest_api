# Generated by Django 5.0.3 on 2024-03-14 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0003_address_pointofcontact_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_end',
            new_name='event_end_time',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_start',
            new_name='event_start_time',
        ),
    ]
