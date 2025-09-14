from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

def user_avatar_path(instance, filename):
    """Return file path for user avatar"""
    ext = filename.split('.')[-1]
    filename = f"{instance.user.username}_{int(now().timestamp())}.{ext}"
    return os.path.join('avatars/', filename)

class Profile(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends only'),
        ('private', 'Private'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public'
    )

    def mutual_friends_with(self, other_profile):
        return self.friends.filter(id__in=other_profile.friends.all())

    def __str__(self):
        return self.user.username

    


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="friend_requests_sent", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="friend_requests_received", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("from_user", "to_user")

    def accept(self):
        self.from_user.profile.friends.add(self.to_user.profile)
        self.to_user.profile.friends.add(self.from_user.profile)
        self.accepted = True
        self.save()

    def decline(self):
        self.delete()

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} (accepted={self.accepted})"

