from django.urls import path
from . import views
urlpatterns = [
    path('write/<str:username>/', views.write_testimonial, name='testimonial_write'),
    path('view/<str:username>/', views.view_testimonials, name='testimonial_list'),
]
