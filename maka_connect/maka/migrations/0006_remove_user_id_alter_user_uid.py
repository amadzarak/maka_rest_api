# Generated by Django 5.0.3 on 2024-03-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0005_eventcheckin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]
