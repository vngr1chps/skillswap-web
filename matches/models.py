from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q

User = settings.AUTH_USER_MODEL
class Reaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions_sent"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reactions_received"
    )
    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"],
                name="unique_reaction"
            )
        ]

    def clean(self):
        if self.from_user_id == self.to_user_id:
            raise ValidationError("Нельзя оценивать самого себя")

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.reaction_type})"


class Match(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_as_user1"
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_as_user2"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user1", "user2"],
                name="unique_match_pair"
            )
        ]

    def clean(self):
        if self.user1_id == self.user2_id:
            raise ValidationError("Матч должен быть между двумя разными пользователями")

    def save(self, *args, **kwargs):
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Match: {self.user1} & {self.user2}"