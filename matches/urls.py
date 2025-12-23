from django.urls import path
from .views import *

urlpatterns = [
    path("", feed_view, name="home"),
    path("like/<int:user_id>", like_view, name="like"),
    path("dislike/<int:user_id>", dislike_view, name="dislike"),
    path("likes/", likes_feed_view, name="likes"),
    path("matches/", matches_view, name="matches")
]