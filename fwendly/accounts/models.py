from django.db import models
from django.contrib.auth.models import User

def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    photo = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def mutual_friends_with(self, other_profile):
        return self.friends.filter(id__in=other_profile.friends.all())
