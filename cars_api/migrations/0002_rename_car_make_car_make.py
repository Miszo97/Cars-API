# Generated by Django 3.2.4 on 2021-06-04 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='car_make',
            new_name='make',
        ),
    ]