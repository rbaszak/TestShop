# Generated by Django 2.1.3 on 2018-11-29 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0003_auto_20181123_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256),
        ),
    ]
