# Generated by Django 4.1.7 on 2023-05-06 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_alter_location_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='districh',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
