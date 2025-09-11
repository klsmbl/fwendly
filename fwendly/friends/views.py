from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FriendRequest
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def friends_list(request):
    profile = request.user.profile
    friends_qs = profile.friends.all()
    paginator = Paginator(friends_qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    incoming = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    outgoing = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, 'friends/friends_list.html', {'page_obj': page_obj, 'incoming': incoming, 'outgoing': outgoing})

@login_required
def send_request(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "You can't add yourself.")
        return redirect('home')
    fr, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=target)
    if created:
        messages.success(request, f"Friend request sent to {target.username}.")
    else:
        messages.info(request, "Friend request already pending.")
    return redirect('home')

@login_required
def accept_request(request, req_id):
    fr = get_object_or_404(FriendRequest, id=req_id, to_user=request.user)
    fr.accept()
    messages.success(request, f"You are now friends with {fr.from_user.username}.")
    return redirect('friends_list')

@login_required
def remove_friend(request, user_id):
    target = get_object_or_404(User, id=user_id)
    request.user.profile.friends.remove(target.profile)
    target.profile.friends.remove(request.user.profile)
    messages.success(request, f"Removed {target.username} from friends.")
    return redirect('friends_list')
