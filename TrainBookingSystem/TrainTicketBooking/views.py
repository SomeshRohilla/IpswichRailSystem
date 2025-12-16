from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Train, Booking


# ================= HOME =================
def home(request):
    return render(request, 'home.html')
# ================= AUTH =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ================= SEARCH TRAINS =================
def search_trains(request):
    trains = Train.objects.all()

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    travel_date = request.GET.get('travel_date')

    if source:
        trains = trains.filter(source__icontains=source)

    if destination:
        trains = trains.filter(destination__icontains=destination)

    if travel_date:
        trains = trains.filter(travel_date=travel_date)

    return render(request, 'search_trains.html', {
        'trains': trains
    })


# ================= BOOK TRAIN =================
@login_required(login_url='login')
def book_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)

    Booking.objects.create(
        user=request.user,
        train=train
    )

    messages.success(request, "🎉 Ticket booked successfully!")
    return redirect('bookings')


# ================= MY BOOKINGS =================
@login_required(login_url='login')
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking.html', {
        'bookings': user_bookings
    })


# ================= DELETE BOOKING =================
@login_required(login_url='login')
def delete_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    booking.delete()
    messages.success(request, "❌ Booking cancelled successfully.")

    return redirect('bookings')
