# Generated by Django 3.2.8 on 2021-12-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_event_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_token',
            field=models.CharField(default='', max_length=500),
        ),
    ]
