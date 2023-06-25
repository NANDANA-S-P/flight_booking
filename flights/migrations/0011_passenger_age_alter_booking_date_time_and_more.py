# Generated by Django 4.2.2 on 2023-06-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0010_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='age',
            field=models.SmallIntegerField(default=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Others')], null=True),
        ),
    ]