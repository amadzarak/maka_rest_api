# Generated by Django 5.0.3 on 2024-03-14 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maka', '0002_rename_user_id_contactpoint_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.TextField()),
                ('address_line_2', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('zip', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PointOfContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('middle_name', models.TextField()),
                ('last_name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='ContactPoint',
            new_name='GuestContact',
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.DateTimeField()),
                ('event_description', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('is_ticketed', models.BooleanField()),
                ('event_start_date', models.DateField()),
                ('is_multi_day', models.BooleanField()),
                ('event_end_date', models.DateField()),
                ('event_start', models.TimeField()),
                ('event_end', models.TimeField()),
                ('cost', models.FloatField()),
                ('host', models.ManyToManyField(to='maka.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maka.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maka.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_time', models.TimeField()),
                ('transaction_date', models.DateField()),
                ('transaction_type', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maka.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.TextField()),
                ('interaction_time', models.DateTimeField()),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to='maka.user')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maka.event')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='maka.user')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.TextField()),
                ('owner', models.TextField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='maka.address')),
                ('point_of_contact', models.ManyToManyField(to='maka.pointofcontact')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ManyToManyField(to='maka.venue'),
        ),
    ]
