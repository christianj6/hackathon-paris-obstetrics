from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model


class RecommendedBuddies(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suggested_buddies = models.ManyToManyField(
        User, blank=True, related_name="suggested_buddies"
    )

    def __str__(self):
        return str(self.user.username)


class InviteBuddy(models.Model):
    to_user = models.ForeignKey(
        User, related_name="to_user", on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE
    )

    def __str__(self):
        return "From {}, to {}".format(
            self.from_user.username, self.to_user.username
        )


class ContentID(models.Model):
    value = models.CharField(max_length=30)

    def __str__(self):
        return self.value


class BuddyBoard(models.Model):
    buddy_1 = models.ForeignKey(
        User, related_name="buddy_1", on_delete=models.CASCADE
    )
    buddy_2 = models.ForeignKey(
        User, related_name="buddy_2", on_delete=models.CASCADE
    )
    buddy_content = models.ManyToManyField(
        ContentID, blank=True, related_name="buddy_content"
    )

    def __str__(self):
        return "Board for {} and {}".format(
            self.buddy_1.username, self.buddy_2.username
        )
