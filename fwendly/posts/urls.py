from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("<str:username>/", views.user_posts, name="user_posts"),
    path("like/<int:post_id>/", views.toggle_post_like, name="toggle_post_like"),
    path("comment/<int:post_id>/", views.add_post_comment, name="add_post_comment"),
]
