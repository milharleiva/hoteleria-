# Generated by Django 4.2.5 on 2023-11-08 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='tipo',
            field=models.CharField(choices=[('sencilla', 'Sencilla'), ('doble', 'Doble'), ('suite', 'Suite')], max_length=50),
        ),
    ]