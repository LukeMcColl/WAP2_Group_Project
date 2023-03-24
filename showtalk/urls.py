from django.urls import path
from . import views

app_name = "showtalk"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("<int:page_id>", views.homepage, name="homepage"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("logout", views.logout, name="logout"),
    path("tv", views.tvv, name="tv"),
    path("pl", views.pinglun, name="pl"),
    path("find-show", views.find_show, name="find-show"),
]
