from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.view_login, name="login"),
    path("sign-up", views.view_signup, name="sign-up"),
    path("logout", views.view_logout, name="logout"),
    path("explore-search", views.view_search, name="explore-search")
]