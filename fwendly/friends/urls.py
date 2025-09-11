from django.urls import path
from . import views
urlpatterns = [
    path('', views.friends_list, name='friends_list'),
    path('add/<int:user_id>/', views.send_request, name='friend_add'),
    path('accept/<int:req_id>/', views.accept_request, name='friend_accept'),
    path('remove/<int:user_id>/', views.remove_friend, name='friend_remove'),
]
