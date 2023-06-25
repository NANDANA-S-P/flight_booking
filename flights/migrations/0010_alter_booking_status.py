# Generated by Django 4.2.2 on 2023-06-25 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0009_booking_flight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(choices=[(0, 'Initiated'), (1, 'Paid'), (2, 'Cancelled'), (3, 'Refunded')]),
        ),
    ]