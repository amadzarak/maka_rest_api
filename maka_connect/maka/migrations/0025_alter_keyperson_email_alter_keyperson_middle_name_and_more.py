# Generated by Django 5.0.3 on 2024-04-10 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0024_rename_point_of_contact_venue_key_persons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyperson',
            name='email',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='keyperson',
            name='middle_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='keyperson',
            name='phone',
            field=models.TextField(null=True),
        ),
    ]
