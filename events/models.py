from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from django.forms import ValidationError
from secrets import token_urlsafe

class event(models.Model):
    user_token = models.CharField(max_length=500, blank=False, default='')
    event_token = models.CharField(max_length=500, blank=False, default='')
    userid = models.IntegerField(blank=False)
    limit = models.IntegerField(blank=False)
    title = models.CharField(max_length=500, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    privacy = models.BooleanField(default=False)
    category = models.TextField()
    description = models.TextField()
    isVirtual = models.BooleanField(default=False)
    location = models.TextField()
    def set_userid(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM knox_authtoken WHERE token_key = %s", [self.user_token[:8]])
            id = cursor.fetchone()
        self.userid = int(id[0])
    
    def set_event_token(self):
        self.event_token = token_urlsafe(16)
    
    def save(self, *args, **kwargs):
        try:
            if not self.userid:
                self.set_userid()
            if not self.event_token:
                self.set_event_token()
            return super(event, self).save(*args, **kwargs)
        except:
            raise ValidationError("This token does not exist!")

    class Meta:
        db_table = 'events'