from django.db import models
from django.contrib.auth.models import User
from db_file_storage.model_utils import delete_file_if_needed

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    image = models.FileField(upload_to="posts/")  # switched from ImageField to FileField
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} ({self.created_at})"

    def liked_by(self, user):
        """Check if a given user liked this post"""
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    def delete(self, *args, **kwargs):
        # make sure image file is deleted from DB if post is deleted
        delete_file_if_needed(self, 'image')
        super().delete(*args, **kwargs)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")  # user can only like once

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"
