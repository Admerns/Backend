from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

# Create your models here.
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = format( reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Shanbe App"),
        # message:
         "کد زیر برای تغییر رمز عبور شما ارسال شده است. \n اگر شما درخواستی برای تغییر رمز عبور خود نداده اید لطفا به این پیام توجه نکنید. \n" + email_plaintext_message,
        # from:
        "noreply@shanbe.local",
        # to:
        [reset_password_token.user.email]
    )


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to="images/userProfile", blank=True ,null = True)
    phone_number = models.CharField(max_length=13)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    def __unicode__(self):
        return self.user.get_full_name()