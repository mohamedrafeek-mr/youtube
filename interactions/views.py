# interactions views might track history, subscriptions, etc.
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import VideoView
from videos.models import Video


@login_required
def subscriptions(request):
    subscribed_profiles = request.user.profile.subscribers.all()
    return render(request, "interactions/subscriptions.html", {"subscribed_profiles": subscribed_profiles})


@login_required
def record_view(request, video_id):
    video = Video.objects.get(id=video_id)
    VideoView.objects.create(user=request.user, video=video)
    return redirect("videos:watch", video_id=video_id)


@login_required
def history(request):
    views = VideoView.objects.filter(user=request.user).select_related('video')[:50]
    return render(request, "interactions/history.html", {"views": views})
