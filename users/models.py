from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default="avatars/human_avatar.png")
    channel_name = models.CharField(max_length=150)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="subscribed_to", blank=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.channel_name} ({self.user.username})"
