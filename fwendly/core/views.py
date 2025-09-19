from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile
from django.core.paginator import Paginator


def home(request):
    if request.user.is_authenticated:
        users_qs = User.objects.exclude(id=request.user.id).order_by('username')
    else:
        users_qs = User.objects.all().order_by('username')
    paginator = Paginator(users_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/home.html', {'page_obj': page_obj})


def profile_view_user(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = target_user.profile
    testimonials = target_user.testimonials_received.all().order_by('-created_at')[:5]

    mutual = None
    if request.user.is_authenticated:
        if request.user == target_user:
            # ✅ If you're viewing your own profile, show all your friends
            mutual = request.user.profile.friends.all()
        else:
            # ✅ Otherwise show mutual friends
            mutual = request.user.profile.mutual_friends_with(profile)

    return render(
        request,
        'core/profile_user.html',
        {
            'profile': profile,
            'mutual': mutual,
            'testimonials': testimonials
        }
    )


def search(request):
    q = request.GET.get('q', '').strip()
    results = User.objects.none()
    if q:
        results = (
            User.objects.filter(username__icontains=q)
            | User.objects.filter(profile__location__icontains=q)
            | User.objects.filter(profile__interests__icontains=q)
        )
        results = results.distinct().order_by('username')
    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/search.html', {'q': q, 'page_obj': page_obj})


# ✅ Helper function inside Profile (put this in accounts/models.py instead of here)
def mutual_friends_with(self, other_profile):
    """
    Return mutual friends queryset between self and another profile
    """
    return self.friends.all().intersection(other_profile.friends.all())


# Attach the method to Profile dynamically (if not already in your model)
Profile.mutual_friends_with = mutual_friends_with

# ✅ Alias so {% url 'profile_user' %} also works in templates
profile_user = profile_view_user
