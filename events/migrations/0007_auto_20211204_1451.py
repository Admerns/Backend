# Generated by Django 3.2.8 on 2021-12-04 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20211204_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='session',
            name='usertoken',
        ),
    ]
