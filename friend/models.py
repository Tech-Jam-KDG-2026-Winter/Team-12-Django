from django.db import models
from accounts.models import User

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

class Friend(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name='friends1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User,
        related_name='friends2',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} & {self.user2}"