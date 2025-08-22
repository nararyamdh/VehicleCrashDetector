from django.db import models

# Create your models here.
class WebAuthnCredential(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    credential_id = models.CharField(max_length=512, unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField(default=0)
    rp_id = models.CharField(max_length=255)
    transports = models.CharField(max_length=255, blank=True, null=True)

class UsersRecorded(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=255, default='unknown@no-organization.com')
    email = models.CharField(max_length=255,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

class AccessKey(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    access_key_1 = models.CharField(max_length=500,unique=True)
    access_key_2 = models.CharField(max_length=500,unique=True)

class WebAuthnCredential_UsersRecorded(models.Model):
    id_x = models.AutoField(primary_key=True,unique=True)
    id_user = models.CharField(max_length=500,unique=True)
    email = models.CharField(max_length=250,unique=True)
