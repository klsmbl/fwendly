from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile, FriendRequest


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
    user_profile = get_object_or_404(Profile, user__username=username)

    # Debug log
    print("DEBUG: Viewing profile of", user_profile.user.username, "visibility:", user_profile.visibility)

    # Case 1: Owner can always view
    if request.user == user_profile.user:
        can_view = True
    else:
        can_view = False
        # Case 2: Public
        if user_profile.visibility == "public":
            can_view = True
        # Case 3: Friends only → allow only if in friends
        elif user_profile.visibility == "friends":
            if user_profile in request.user.profile.friends.all():
                can_view = True
        # Case 4: Private → never allow unless owner (already handled above)

    # If not allowed → show private_profile.html
    if not can_view:
        return render(request, "accounts/private_profile.html", {
            "user_profile": user_profile
        })

    # Normal profile view
    mutual_qs = request.user.profile.mutual_friends_with(user_profile)
    mutual_count = mutual_qs.count()  # ✅ number of mutual friends

    already_friend = user_profile in request.user.profile.friends.all()
    outgoing_request = FriendRequest.objects.filter(
        from_user=request.user, to_user=user_profile.user, accepted=False
    ).first()
    incoming_request = FriendRequest.objects.filter(
        from_user=user_profile.user, to_user=request.user, accepted=False
    ).first()

    return render(request, "accounts/profile_view_user.html", {
        "user_profile": user_profile,
        "already_friend": already_friend,
        "outgoing_request": outgoing_request,
        "incoming_request": incoming_request,
        "mutual": mutual_qs,          # full list if you want to show actual names
        "mutual_count": mutual_count, # ✅ count for "You have X mutual friends"
    })