# Generated by Django 3.2.8 on 2021-11-30 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_session_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='limit',
        ),
    ]