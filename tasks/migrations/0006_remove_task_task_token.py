# Generated by Django 3.2.8 on 2021-11-09 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_task_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_token',
        ),
    ]
