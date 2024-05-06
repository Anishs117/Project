# Generated by Django 5.0.4 on 2024-05-06 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='average_response_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='fulfillment_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='quality_rating_avg',
            field=models.FloatField(default=0.0),
        ),
    ]