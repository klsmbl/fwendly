from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    author = models.ForeignKey(User, related_name='testimonials_written', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='testimonials_received', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author} for {self.target}"
