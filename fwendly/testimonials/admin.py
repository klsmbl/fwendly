from django.contrib import admin
from .models import Testimonial
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author','target','created_at')
    search_fields = ('author__username','target__username','content')
