from django.shortcuts import render
from videos.models import Video


def home(request):
    # Show all published videos on home page
    latest = Video.objects.filter(status="published").order_by("-created_at")
    return render(request, "core/home.html", {"latest_videos": latest})
