from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("profile_view_user", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})

def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by("-created_at")
    return render(request, "posts/user_posts.html", {"user": user, "posts": posts})
