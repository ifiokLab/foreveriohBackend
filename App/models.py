from django.db import models
from django.conf import settings
# Create your models here.

from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

'''deceased>>memorial>>biography'''


class myuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40,blank=False)
    last_name = models.CharField(max_length=40,blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Deceased(models.Model):
    TYPE_CHOICES = (
        ('mother', 'mother'),
        ('father', 'father'),
        ('brother', 'brother'),
        ('sister', 'sister'),
        ('nephew', 'nephew'),
        ('cousin', 'cousin'),
        ('neice', 'neice'),
        ('grand mother', 'grand mother'),
        ('grand father', 'grand father'),
    )
    Audience_CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private'),

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null =True,blank = True)
    #contributors = models.ManyToManyField(Contributor, blank=True,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100,blank=True,null=True)
    relationship_type = models.CharField(choices=TYPE_CHOICES, max_length=20,blank=True,null=True)
    audience = models.CharField(choices=Audience_CHOICES, max_length=20,default = "Public")
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    cover_photo = models.ImageField(upload_to='cover-photo/',default='cover-photo/profile.jpg')
    heart = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_cover', blank=True, null = True)
    share = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='share', blank=True,null = True)

    



    def __str__(self):
        return self.first_name






from django.utils import timezone

class Tribute(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deceased = models.ForeignKey(Deceased,on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tribute', blank=True)
    heart = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='heart_tribute', blank=True)

    def get_time_since_comment(self):
        time_difference = timezone.now() - self.date

        if time_difference.total_seconds() < 60:  # Less than a minute
            return f"{int(time_difference.total_seconds())} sec ago"
        elif time_difference.total_seconds() < 3600:  # Less than an hour
            minutes = int(time_difference.total_seconds() / 60)
            return f"{minutes} mins ago"
        elif time_difference.total_seconds() < 86400:  # Less than a day
            hours = int(time_difference.total_seconds() / 3600)
            return f"{hours} hours ago"
        elif time_difference.total_seconds() < 604800:  # Less than a week
            days = int(time_difference.total_seconds() / 86400)
            return f"{days} days ago"
        elif time_difference.total_seconds() < 2592000:  # Less than a month
            weeks = int(time_difference.total_seconds() / 604800)
            return f"{weeks} weeks ago"
        elif time_difference.total_seconds() < 31536000:  # Less than a year
            months = int(time_difference.total_seconds() / 2592000)
            return f"{months} months ago"
        else:
            years = int(time_difference.total_seconds() / 31536000)
            return f"{years} years ago"



    class Meta:
        ordering = ['-id']



class TributeReply(models.Model):
    tribute = models.ForeignKey(Tribute, on_delete=models.CASCADE, related_name='tribute_replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tribute_liked_reply', blank=True)
    heart = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tribute_heart_reply', blank=True)


    def get_time_since_comment(self):
        time_difference = timezone.now() - self.date

        if time_difference.total_seconds() < 60:  # Less than a minute
            return f"{int(time_difference.total_seconds())} sec ago"
        elif time_difference.total_seconds() < 3600:  # Less than an hour
            minutes = int(time_difference.total_seconds() / 60)
            return f"{minutes} mins ago"
        elif time_difference.total_seconds() < 86400:  # Less than a day
            hours = int(time_difference.total_seconds() / 3600)
            return f"{hours} hours ago"
        elif time_difference.total_seconds() < 604800:  # Less than a week
            days = int(time_difference.total_seconds() / 86400)
            return f"{days} days ago"
        elif time_difference.total_seconds() < 2592000:  # Less than a month
            weeks = int(time_difference.total_seconds() / 604800)
            return f"{weeks} weeks ago"
        elif time_difference.total_seconds() < 31536000:  # Less than a year
            months = int(time_difference.total_seconds() / 2592000)
            return f"{months} months ago"
        else:
            years = int(time_difference.total_seconds() / 31536000)
            return f"{years} years ago"


