from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_view(request):
    profile = request.user.profile
    testimonials = request.user.testimonials_received.all()
    return render(request, 'accounts/profile.html', {'profile': profile, 'testimonials': testimonials})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
