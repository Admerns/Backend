from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from django.forms import ValidationError
from secrets import token_urlsafe

class event(models.Model):
    user_token = models.CharField(max_length=500, blank=False, default='')
    event_token = models.CharField(max_length=500, blank=False, default='')
    userid = models.IntegerField(blank=False)
    title = models.CharField(max_length=500, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    privacy = models.BooleanField(default=False)
    category = models.TextField()
    description = models.TextField()
    isVirtual = models.BooleanField(default=False)
    address = models.TextField(blank=True, default='')
    link = models.TextField(blank=True, default='')
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

class session (models.Model):
    session_token = models.CharField(max_length=500, blank=False, default='')
    limit = models.IntegerField(blank=False)
    filled = models.IntegerField(blank=False, default=0)
    time = models.TextField()
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    users = models.ManyToManyField(User,related_name='user_sessions')

    def set_session_token(self):
        self.session_token = token_urlsafe(16)
    
    def save(self, *args, **kwargs):
        try:
            if not self.session_token:
                self.set_session_token()
            return super(session, self).save(*args, **kwargs)
        except:
            raise ValidationError("Session token initialization error!")