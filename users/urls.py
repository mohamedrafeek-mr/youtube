from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("channel/<str:username>/", views.channel, name="channel"),
    path("subscribe/<str:username>/", views.subscribe, name="subscribe"),
]
