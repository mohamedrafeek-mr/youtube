from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from django.contrib.auth.models import User
from .forms import VideoUploadForm
from django.contrib import messages
from comments.models import Comment
from comments.views import add_comment, delete_comment


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.status = 'processing'
            video.save()
            messages.success(request, 'Video uploaded and queued for processing.')
            return redirect('videos:upload')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = VideoUploadForm()
    return render(request, "videos/upload.html", {"form": form})


def watch(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save(update_fields=["views"])

    related = (
        Video.objects.filter(status="published").exclude(id=video.id)
        .order_by("-views")[:10]
    )

    liked = False
    if request.user.is_authenticated:
        liked = request.user in video.likes.all()

    uploader_profile = None
    try:
        from users.models import Profile
        uploader_profile = Profile.objects.filter(user=video.uploader).first()
    except Exception:
        uploader_profile = None

    if request.user.is_authenticated:
        try:
            from interactions.models import VideoView
            VideoView.objects.create(user=request.user, video=video)
        except Exception:
            pass

    # Fetch comments for this video
    comments = Comment.objects.filter(video=video).order_by('-created_at')

    return render(
        request,
        "videos/watch.html",
        {
            "video": video,
            "related_videos": related,
            "liked": liked,
            "uploader_profile": uploader_profile,
            "comments": comments,
        },
    )


def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user.is_authenticated:
        if request.user in video.likes.all():
            video.likes.remove(request.user)
        else:
            video.likes.add(request.user)
    return redirect("videos:watch", video_id=video_id)


def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user.is_authenticated:
        if request.user in video.likes.all():
            video.likes.remove(request.user)
    return redirect("videos:watch", video_id=video_id)


@login_required
def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, uploader=request.user)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully.')
            return redirect('users:channel', username=request.user.username)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = VideoUploadForm(instance=video)
    return render(request, "videos/upload.html", {"form": form, "editing": True})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, uploader=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully.')
        return redirect('users:channel', username=request.user.username)
    return render(request, "videos/delete.html", {"video": video})
