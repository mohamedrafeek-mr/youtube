from django.contrib import admin
from .models import VideoView


@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "viewed_at")
    list_filter = ("viewed_at",)
