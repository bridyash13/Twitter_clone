from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class UserModel(AbstractUser):
    name = models.CharField(max_length=30, default='')
    email = models.CharField(max_length=30,null=False)
    uname = models.CharField(max_length=200,default='',unique=True,null=False)
    password = models.CharField(max_length=200,default='',null=False)
    password2 = models.CharField(max_length=200,default='',null=False)
    bio = models.CharField(max_length=200,default='',blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    USERNAME_FIELD = 'uname'
    REQUIRED_FIELDS = ['email', 'username']

    def __str__(self):
        return self.uname

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Meep(models.Model):
    meepid = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(UserModel,on_delete=models.CASCADE,default=None)
    meeptext = models.CharField(max_length=200,default='',null=False)
    meep_time = models.DateTimeField(default=now, editable=False)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return str(self.userid.uname) + ": " + str(self.meeptext)


class Follower(models.Model):
    follower = models.ForeignKey(UserModel,on_delete=models.CASCADE,default=None,null=True, blank=True)
    person =  models.CharField(max_length=200,default='')

    def __str__(self):
        return str(self.follower) + " follows " + str(self.person)



