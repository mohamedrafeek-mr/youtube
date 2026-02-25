from django.urls import path
from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.list_playlists, name="list"),
    path("create/", views.create_playlist, name="create"),
    path("<int:playlist_id>/", views.detail, name="detail"),
    path("<int:playlist_id>/add/<int:video_id>/", views.add_video, name="add_video"),
    path("<int:playlist_id>/edit/", views.edit_playlist, name="edit"),
    path("<int:playlist_id>/delete/", views.delete_playlist, name="delete"),
]
