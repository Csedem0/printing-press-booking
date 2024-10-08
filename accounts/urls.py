# printing_press_booking/urls.py

from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.index, name='home'),
    path('indexa/', views.indexa, name='indexa'),
    path('press/<int:press_id>/book/', views.make_booking, name='make_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),

    # Authentication
    path('register/', views.register_customer, name='register'),
    path('register-owner/', views.register_owner, name='register_owner'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
