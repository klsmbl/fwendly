from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TestimonialForm
from .models import Testimonial
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@login_required
def write_testimonial(request, username):
    target = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.target = target
            t.save()
            messages.success(request, 'Testimonial posted!')
            return redirect('profile_view_user', username=username)
    else:
        form = TestimonialForm()
    return render(request, 'testimonials/write.html', {'form': form, 'target': target})

def view_testimonials(request, username):
    target = get_object_or_404(User, username=username)
    testimonials_qs = target.testimonials_received.all().order_by('-created_at')
    paginator = Paginator(testimonials_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'testimonials/list.html', {'page_obj': page_obj, 'target': target})



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Testimonial, Comment

@login_required
def add_comment(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                testimonial=testimonial,
                author=request.user,
                content=content
            )
            messages.success(request, "Comment added!")
    # redirect to the correct testimonial list page
    return redirect('testimonial_list', username=testimonial.target.username)

