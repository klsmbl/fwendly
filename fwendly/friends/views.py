from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import FriendRequest, Profile

@login_required
def friends_list(request):
    profile = request.user.profile
    friends_qs = profile.friends.all()
    paginator = Paginator(friends_qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    incoming = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    outgoing = FriendRequest.objects.filter(from_user=request.user, accepted=False)

    return render(request, 'friends/friends_list.html', {
        'page_obj': page_obj,
        'incoming': incoming,
        'outgoing': outgoing
    })

@login_required
def send_request(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "You can't add yourself.")
        return redirect('home')

    if target.profile in request.user.profile.friends.all():
        messages.info(request, f"You are already friends with {target.username}.")
        return redirect('home')

    fr, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=target)
    if created:
        messages.success(request, f"Friend request sent to {target.username}.")
    else:
        messages.info(request, "Friend request already pending.")
    return redirect('home')

@login_required
def accept_request(request, req_id):  # <--- must match URL
    friend_request = get_object_or_404(FriendRequest, id=req_id)
    
    if friend_request.to_user == request.user:
        # Add each other as friends
        request.user.profile.friends.add(friend_request.from_user.profile)
        friend_request.from_user.profile.friends.add(request.user.profile)

        # Delete the friend request
        friend_request.delete()

    return redirect('friends_list')

@login_required
def decline_request(request, req_id):
    fr = get_object_or_404(FriendRequest, id=req_id, to_user=request.user, accepted=False)
    fr.decline()
    messages.info(request, f"Friend request from {fr.from_user.username} declined.")
    return redirect('friends_list')

@login_required
def cancel_request(request, req_id):
    fr = get_object_or_404(FriendRequest, id=req_id, from_user=request.user, accepted=False)
    fr.delete()
    messages.info(request, f"Friend request to {fr.to_user.username} cancelled.")
    return redirect('friends_list')

@login_required
def remove_friend(request, user_id):
    target = get_object_or_404(User, id=user_id)
    request.user.profile.friends.remove(target.profile)
    target.profile.friends.remove(request.user.profile)
    messages.success(request, f"Removed {target.username} from friends.")
    return redirect('friends_list')

@login_required
def friend_add(request, user_id):
    to_profile = get_object_or_404(Profile, id=user_id)

    # Prevent sending to self
    if to_profile.user == request.user:
        messages.warning(request, "You cannot send a friend request to yourself.")
        return redirect('profile_view_user', username=request.user.username)

    # Check if the request already exists
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_profile.user).exists():
        messages.info(request, "Friend request already sent.")
        return redirect('profile_view_user', username=to_profile.user.username)

    FriendRequest.objects.create(
        from_user=request.user,
        to_user=to_profile.user
    )
    messages.success(request, f"Friend request sent to {to_profile.user.username}!")
    return redirect('profile_view_user', username=to_profile.user.username)

def friends_list(request):
    user_profile = request.user.profile

    # Friends
    friends_qs = user_profile.friends.all().order_by('user__username')
    paginator = Paginator(friends_qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Friend Requests
    incoming = FriendRequest.objects.filter(to_user=request.user)
    outgoing = FriendRequest.objects.filter(from_user=request.user)

    # Prepare friend data with flags for template
    friends_data = []
    for f in page_obj:
        friends_data.append({
            'user': f.user,
            'location': getattr(f, 'location', ''),
            'is_friend': True,
            'has_incoming_request': incoming.filter(from_user=f.user).exists(),
            'has_outgoing_request': outgoing.filter(to_user=f.user).exists(),
        })

    return render(request, 'friends/friends_list.html', {
        'page_obj': friends_data,
        'incoming': incoming,
        'outgoing': outgoing
    })