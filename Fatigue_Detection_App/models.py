from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import uuid


#=========== User Model ===========
class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Worker"),)
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class Admin(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    admin_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic = models.FileField(default="/media/admin/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Worker(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    worker_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    supervisor_email = models.EmailField(null=True)
    profile_pic = models.FileField(default="/media/worker/user.png")
    device_token = models.CharField(max_length=200, null=True)
    last_fatigue_state = models.DateTimeField(null=True)
    jwt = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Fatigue_State(models.Model):
    fatigue_state_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fatigue_state_worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    fatigue_state = models.CharField(max_length=20, null=True)
    fatigue_state_created_at = models.DateTimeField(auto_now_add=True)
    fatigue_state_updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#============= Creating signals ============
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(user=instance)
        if instance.user_type==2:
            Worker.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.worker.save()
