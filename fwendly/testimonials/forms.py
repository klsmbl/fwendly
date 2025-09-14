from django import forms
from .models import Testimonial, Comment
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows':4, 'class':'w-full p-2 border rounded'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }