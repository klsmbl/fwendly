from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile, FriendRequest  # Fixed import

@login_required
def profile_view(request):
    profile = request.user.profile
    testimonials = request.user.testimonials_received.all()
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'testimonials': testimonials
    })

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

@login_required
def profile_view_user(request, username):
    # View another user's profile
    user_profile = get_object_or_404(Profile, user__username=username)

    # Mutual friends (optional)
    mutual = request.user.profile.mutual_friends_with(user_profile)

    # Friendship checks
    already_friend = user_profile in request.user.profile.friends.all()
    outgoing_request = FriendRequest.objects.filter(
        from_user=request.user, to_user=user_profile.user, accepted=False
    ).first()
    incoming_request = FriendRequest.objects.filter(
        from_user=user_profile.user, to_user=request.user, accepted=False
    ).first()

    return render(request, 'accounts/profile_view_user.html', {
        'user_profile': user_profile,
        'already_friend': already_friend,
        'outgoing_request': outgoing_request,
        'incoming_request': incoming_request,
        'mutual': mutual,
    })

    # Calculate mutual friends
    mutual = user_profile.mutual_friends_with(request.user.profile)

    return render(request, 'accounts/profile_view_user.html', {
        'user_profile': user_profile,
        'already_friend': already_friend,
        'outgoing_request': outgoing_request,
        'incoming_request': incoming_request,
        'mutual': mutual,
    })
