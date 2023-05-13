from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.view_login, name="login"),
    path("sign-up", views.view_signup, name="sign-up"),
    path("logout", views.view_logout, name="logout"),
    path("explore-search", views.view_search, name="explore-search"),
    path("reservation/<int:reservation_id>", views.view_reservation, name="reservation"),
    path("provider/<int:provider_id>", views.view_provider, name="provider"),
    path("subscribe", views.view_subscribe, name="subscribe"),
    path("unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("cancel-reservation", views.cancel_reservation, name="cancel-reservation"),
    path("new-reservation/<int:provider_id>", views.view_new_reservation, name="new-reservation")
]