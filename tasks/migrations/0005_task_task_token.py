# Generated by Django 3.2.8 on 2021-11-06 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_token',
            field=models.CharField(default='', max_length=500),
        ),
    ]
