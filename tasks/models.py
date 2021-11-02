from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from django.forms import ValidationError

# Create your models here.
class task(models.Model):
    user_token = models.CharField(max_length=500, blank=False, default='')
    userid = models.IntegerField(blank=False)
    title = models.CharField(max_length=500, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    category = models.TextField()
    description = models.TextField()
    alarm_check = models.TextField()
    push_notification = models.TextField()

    class Meta:
        db_table = 'tasks'