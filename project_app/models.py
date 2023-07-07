from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile_number = models.CharField(max_length=20,null=True,blank=True)


class Account_Otp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    otp = models.IntegerField(default=0)


class Lgin_otp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    otp = models.IntegerField(default=0)


class All_Images(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    image = models.FileField(upload_to='all_images',null=True,blank=True)
    image_name = models.CharField(max_length=100)
    check_status =models.BooleanField(default=False) 


class InterstedImages(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    images_id =models.IntegerField(default=0)
    click_time = models.DateTimeField(auto_now_add=True)
    visit_time = models.DateTimeField(auto_now=True)


class RejectedImages(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    images_id =models.IntegerField(default=0)
    click_time = models.DateTimeField(auto_now_add=True)

class UserHistory(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    all_images = models.ForeignKey(All_Images,on_delete=models.DO_NOTHING,null=True,blank=True)
    click_time = models.DateTimeField(auto_now_add=True)
    is_reject = models.BooleanField(default="False")
    is_selected = models.BooleanField(default='False')

