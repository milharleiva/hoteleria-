# Generated by Django 4.2.5 on 2023-11-09 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0002_alter_habitacion_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='precio',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
