from django.db import models

# Create your models here.
class task(models.Model):
    userid = models.IntegerField(blank=False)
    title = models.CharField(max_length=500, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    category = models.TextField()
    description = models.TextField()
    alarm_check = models.TextField()
    push_notification = models.TextField()

    class Meta:
        db_table = 'tasks'