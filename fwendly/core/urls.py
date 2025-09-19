from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('user/<str:username>/', views.profile_view_user, name='profile_view_user'),
    path('search/user/<str:username>/', views.profile_view_user, name='profile_view_user_search'),
    # ✅ Alias so templates using 'profile_user' still work
    path('u/<str:username>/', views.profile_view_user, name='profile_user'),
]