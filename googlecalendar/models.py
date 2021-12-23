from django.db import models

# Create your models here.

class google_calendar(models.Model):
    userid = models.IntegerField(blank=False)
    access_token = models.CharField(max_length=500, blank=False)
    refresh_token = models.CharField(max_length=500, blank=False)

    class Meta:
        db_table = 'google_calendar'