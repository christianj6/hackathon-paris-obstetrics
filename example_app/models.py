from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Users

class Content_Item(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_accessed = models.DateTimeField(default=timezone.now)
	# work with this a bit to feed to our algo
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

# class Interest(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE) # find how to generate this info like a post and keep updating it
# 	content = models.TextField()		# this will just be a python dict we can keep updating as needed

# 	def __str__(self):
# 		return self.user 

class Content(models.Model):
	source_title = models.CharField(max_length=100)
	source_url = models.TextField()
	topics = models.TextField()
	text = models.TextField()
	images = models.TextField()

	def __str__(self):
		return self.topics 