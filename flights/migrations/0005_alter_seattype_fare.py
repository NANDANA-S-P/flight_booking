# Generated by Django 4.2.2 on 2023-06-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_seat_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seattype',
            name='fare',
            field=models.IntegerField(),
        ),
    ]
