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

    # ✅ Precompute if the current user liked each post
    if request.user.is_authenticated:
        for post in posts:
            post.liked_by_user = post.likes.filter(user=request.user).exists()
    else:
        for post in posts:
            post.liked_by_user = False

    return render(request, "posts/user_posts.html", {"user": user, "posts": posts})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostComment, PostLike

@login_required
def add_post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            PostComment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, "Comment added!")
    return redirect("user_posts", username=post.user.username)

@login_required
def toggle_post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        # already liked → unlike
        like.delete()

    return redirect(request.META.get("HTTP_REFERER", "profile"))
