# Generated by Django 4.1.7 on 2023-05-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_providersettings_logo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providersettings',
            name='logo_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
