from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.utils import timezone

# Create your models here.
class FileUploads(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50, default = '')
	file = models.FileField(upload_to='media/')
	content = models.TextField()
	summary = models.CharField(max_length = 150, default = '')
	created_at = models.DateTimeField(auto_now=True)

	




