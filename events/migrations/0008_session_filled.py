# Generated by Django 3.2.8 on 2021-12-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20211204_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='filled',
            field=models.IntegerField(default=0),
        ),
    ]
