from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .services import *

User = get_user_model()

@login_required
def feed_view(request):
    user = request.user

    feed_users = get_user_feed(user, limit=5)

    context = {
        "feed_users": feed_users
    }

    return render(request, "home/home.html", context)


@login_required
@require_POST
def like_view(request, user_id):

    from_user = request.user
    to_user = get_object_or_404(User, id=user_id)
    like_user(from_user, to_user)
    return redirect("home")


@login_required
@require_POST
def dislike_view(request, user_id):

    from_user = request.user
    to_user = get_object_or_404(User, id=user_id)
    dislike_user(from_user, to_user)
    return redirect("home")


@login_required
def likes_feed_view(request):
    user = request.user
    likes = get_who_liked(user)

    context = {
        "likes": likes
    }
    return render(request, "home/likes.html", context)


@login_required
def matches_view(request):
    user = request.user

    matches = get_matches(user)

    context = {
        "matches": matches
    }
    return render(request, "home/matches.html", context)