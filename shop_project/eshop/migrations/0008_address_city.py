# Generated by Django 2.1.3 on 2019-01-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0007_auto_20181201_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
    ]
