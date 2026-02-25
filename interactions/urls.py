from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("record/<int:video_id>/", views.record_view, name="record"),
    path("history/", views.history, name="history"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
]
