from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path("upload/", views.upload_video, name="upload"),
    path("<int:video_id>/", views.watch, name="watch"),
    path("<int:video_id>/like/", views.like_video, name="like"),
    path("<int:video_id>/dislike/", views.dislike_video, name="dislike"),
    path("<int:video_id>/edit/", views.edit_video, name="edit"),
    path("<int:video_id>/delete/", views.delete_video, name="delete"),
    path("<int:video_id>/add_comment/", views.add_comment, name="add_comment"),
    path("<int:video_id>/delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
]
