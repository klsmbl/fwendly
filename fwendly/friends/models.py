from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        self.from_user.profile.friends.add(self.to_user.profile)
        self.to_user.profile.friends.add(self.from_user.profile)
        self.accepted = True
        self.save()

    def decline(self):
        self.delete()

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} (accepted={self.accepted})"
