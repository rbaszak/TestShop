# Generated by Django 2.1.3 on 2018-12-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0006_auto_20181201_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
