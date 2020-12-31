
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import User


class Document(models.Model):
    #image_path = os.path.join(settings.BASE_DIR, 'images')
    #docfile = models.ImageField(upload_to='')
    docfile = models.FileField(upload_to='images/')



class PictureSubmission(models.Model):
	User =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	PicLocation = models.CharField(max_length=60)
	Date = models.DateField()

	class Meta:

		indexes=[models.Index(fields=['User','Date'])]

class VideoSubmission(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	Date= models.DateField()

class Thread(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	Date= models.DateField(auto_now_add=True)
	Title = models.CharField(max_length=30)
	Description = models.TextField()
	Topic = models.CharField(max_length=30)

class Comment(models.Model):
	
	User = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	Date= models.DateField(auto_now_add=True)
	Description = models.TextField()
	Thread = models.ForeignKey(Thread, on_delete=models.CASCADE)


class PictureUser(models.Model):

	User = models.OneToOneField(User, on_delete=models.CASCADE)
	LastDateUsed = models.DateField()
	TimesUsedToday = models.IntegerField()

class VideoUser(models.Model):

	User = models.OneToOneField(User, on_delete=models.CASCADE)
	LastDateUsed = models.DateField()
	TimesUsedToday = models.IntegerField()
