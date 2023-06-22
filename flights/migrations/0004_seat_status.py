# Generated by Django 4.2.2 on 2023-06-22 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_airline_added_at_airline_added_by_airport_added_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='status',
            field=models.IntegerField(choices=[(0, 'Available'), (1, 'Booked')], default=0),
        ),
    ]