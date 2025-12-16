from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home' ),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_trains, name='search_trains'),
    path('bookings/', views.bookings, name='bookings'),
    path('book/<int:train_id>/', views.book_train, name='book_train'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    
 
]
