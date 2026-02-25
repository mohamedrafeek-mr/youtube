from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from videos.models import Video


@login_required
def add_comment(request, video_id):
    if request.method == "POST":
        text = request.POST.get("text", "")
        video = get_object_or_404(Video, id=video_id)
        Comment.objects.create(video=video, user=request.user, text=text)
    return redirect("videos:watch", video_id=video_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    video_id = comment.video.id
    comment.delete()
    return redirect("videos:watch", video_id=video_id)
