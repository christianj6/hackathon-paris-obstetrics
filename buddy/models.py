from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

# from django.conf import settings


# rec user model which suggests the users for pairing

	# pair_users
		# keyed to each user




class RecommendedBuddies(models.Model):

# 		# parse the practice db based on user's values
# 		# exclude self
# 		# suggest whatever other users according to relevant params
# 		# return the list of relevant users
# 		# will need to update this model when user updates prof

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suggested_buddies = models.ManyToManyField(User, blank=True, related_name='suggested_buddies')
    slug = models.SlugField()

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
    	return "/users/{}".format(self.slug)

class InviteBuddy(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)

# class InviteBuddy(models.Model):
# 	to_user = models.ForeignKey()
# 	from_user = models.OneToOneField(User, on_delete=models.CASCADE)

# class BoardBuddy(models.Model):
	# this will pair a user with a single buddy
	# and store all the content that is displayed on the board page
	# # board model which stores the content from the paired users
