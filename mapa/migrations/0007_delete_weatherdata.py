# Generated by Django 4.2.17 on 2025-02-26 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapa', '0006_remove_weatherdata_description_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WeatherData',
        ),
    ]
