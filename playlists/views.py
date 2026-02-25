from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Playlist
from videos.models import Video


@login_required
def list_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "playlists/list.html", {"playlists": playlists})


@login_required
def create_playlist(request):
    if request.method == "POST":
        name = request.POST.get("name")
        is_public = bool(request.POST.get("is_public"))
        playlist = Playlist.objects.create(user=request.user, name=name, is_public=is_public)
        return redirect("playlists:detail", playlist_id=playlist.id)
    return render(request, "playlists/create.html")


@login_required
def add_video(request, playlist_id, video_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    video = get_object_or_404(Video, id=video_id)
    playlist.videos.add(video)
    return redirect("playlists:detail", playlist_id=playlist_id)


@login_required
def detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return render(request, "playlists/detail.html", {"playlist": playlist})


@login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    if request.method == "POST":
        playlist.name = request.POST.get("name")
        playlist.is_public = bool(request.POST.get("is_public"))
        playlist.save()
        return redirect("playlists:detail", playlist_id=playlist.id)
    return render(request, "playlists/edit.html", {"playlist": playlist})


@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    playlist.delete()
    return redirect("users:channel", username=request.user.username)
