# Generated by Django 4.1.7 on 2023-05-06 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceprovider',
            name='location',
        ),
    ]
