from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Profile
from videos.models import Video


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, channel_name=user.username)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("core:home")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("core:home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("core:home")


def channel(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    videos = Video.objects.filter(uploader=user, status='published').order_by('-created_at')
    return render(request, "users/channel.html", {"profile": profile, "videos": videos})


@login_required
def subscribe(request, username):
    target = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=target)
    profile.subscribers.add(request.user)
    return redirect("users:channel", username=username)
