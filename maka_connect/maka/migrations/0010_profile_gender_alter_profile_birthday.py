# Generated by Django 5.0.3 on 2024-03-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0009_alter_profile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
