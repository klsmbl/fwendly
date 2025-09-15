from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    author = models.ForeignKey(User, related_name='testimonials_written', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='testimonials_received', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name="testimonial_likes", blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Testimonial by {self.author} for {self.target}"

class Comment(models.Model):
    testimonial = models.ForeignKey(Testimonial, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments_written", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.testimonial}"