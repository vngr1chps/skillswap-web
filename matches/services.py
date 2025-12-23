from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.db import IntegrityError
from .models import Reaction, Match
from django.contrib.auth import get_user_model

User = get_user_model()

@transaction.atomic
def like_user(from_user, to_user):
    if from_user.id == to_user.id:
        raise ValueError("Нельзя лайкать самого себя")

    try:
        reaction, created = Reaction.objects.update_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={"reaction_type": Reaction.LIKE},
        )
    except IntegrityError:
        reaction = Reaction.objects.filter(
            from_user=from_user,
            to_user=to_user
        ).first()
        created = False

        if reaction is None:
            reaction = Reaction.objects.create(
                from_user=from_user,
                to_user=to_user,
                reaction_type=Reaction.LIKE,
            )
            created = True

        elif reaction.reaction_type != Reaction.LIKE:
            reaction.reaction_type = Reaction.LIKE
            reaction.save(update_fields=["reaction_type"])


    is_mutual = Reaction.objects.filter(
        from_user=to_user,
        to_user=from_user,
        reaction_type=Reaction.LIKE,
    ).exists()

    match = None
    match_created = False


    if is_mutual:
        user1, user2 = sorted([from_user, to_user], key=lambda u: u.id)

        try:
            match, match_created = Match.objects.get_or_create(
                user1=user1, user2=user2
            )
        except IntegrityError:
            match = Match.objects.filter(user1=user1, user2=user2).first()
            match_created = False

    return {
        "reaction": reaction,
        "reaction_created": created,
        "is_mutual": is_mutual,
        "match": match,
        "match_created": match_created,
    }
    

@transaction.atomic
def dislike_user(from_user, to_user):
    if from_user.id == to_user.id:
        raise ValueError("Нельзя дизлайкать самого себя")
    try:
        reaction, created = Reaction.objects.update_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={"reaction_type": Reaction.DISLIKE}
        )
    except IntegrityError:
        reaction = Reaction.objects.filter(
            from_user=from_user,
            to_user=to_user,
        ).first()
        created = False

        if reaction is None:
            reaction = Reaction.objects.create(
                from_user=from_user,
                to_user=to_user,
                reaction_type=Reaction.DISLIKE
            )
            created = True

        elif reaction.reaction_type != Reaction.DISLIKE:
            reaction.reaction_type = Reaction.DISLIKE
            reaction.save(update_fields=["reaction_type"])
    return {
        "reaction": reaction,
        "reaction_created": created,
    }


def get_user_feed(user, limit=5):
    all_users = User.objects.exclude(id=user.id)
    unwanted_users = Reaction.objects.filter(from_user=user).values_list("to_user_id", flat=True)
    filtred_feed = all_users.exclude(id__in=unwanted_users)
    return filtred_feed[:limit]

def get_who_liked(user):
    liked_by_user_ids = Reaction.objects.filter(
        to_user=user,
        reaction_type=Reaction.LIKE
    ).values_list("from_user_id", flat=True)

    reacted_to_ids = Reaction.objects.filter(from_user=user).values_list("to_user_id", flat=True)

    return User.objects.filter(id__in=liked_by_user_ids).exclude(id__in=reacted_to_ids)


def get_matches(user):
    matches = Match.objects.filter(Q(user1=user) | Q(user2=user))
    users = []

    for match in matches:
        if match.user1 == user:
            users.append(match.user2)
        else:
            users.append(match.user1)
    return users
