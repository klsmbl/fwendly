from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_list, name='friends_list'),
    path('send/<int:user_id>/', views.send_request, name='send_request'),
    path('accept/<int:req_id>/', views.accept_request, name='accept_request'),
    path('decline/<int:req_id>/', views.decline_request, name='decline_request'),
    path('cancel/<int:req_id>/', views.cancel_request, name='cancel_request'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('add/<int:user_id>/', views.friend_add, name='friend_add'),
]
