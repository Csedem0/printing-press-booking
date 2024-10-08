# booking/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import PrintingPress, Booking
from .forms import UserRegistrationForm, PrintingPressOwnerForm, BookingForm

def index(request):
    presses = PrintingPress.objects.all()
    return render(request, 'index.html', {'presses': presses})

def indexa(request):
    presses = PrintingPress.objects.all()
    return render(request, 'indexa.html', {'presses': presses})

@login_required
def make_booking(request, press_id):
    press = PrintingPress.objects.get(id=press_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.printing_press = press
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'make_booking.html', {'form': form, 'press': press})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def manage_bookings(request):
    bookings = Booking.objects.filter(printing_press__owner=request.user)
    return render(request, 'manage_bookings.html', {'bookings': bookings})

# Customer registration
def register_customer(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Customer Registration'})

# Press owner registration with atomic transaction
@transaction.atomic
def register_owner(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        owner_form = PrintingPressOwnerForm(request.POST)
        if user_form.is_valid() and owner_form.is_valid():
            # Start atomic transaction to ensure both user and press are created
            try:
                # Save user
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                
                # Save PrintingPress with linked user
                press = owner_form.save(commit=False)
                press.owner = user
                press.save()

                # Automatically log in the user
                login(request, user)
                return redirect('home')
            except Exception as e:
                transaction.set_rollback(True)  # Rollback if anything fails
                return render(request, 'registration/register_owner.html', {
                    'user_form': user_form,
                    'owner_form': owner_form,
                    'error': str(e),  # Display error message
                    'title': 'Press Owner Registration'
                })
    else:
        user_form = UserRegistrationForm()
        owner_form = PrintingPressOwnerForm()
    
    return render(request, 'registration/register_owner.html', {
        'user_form': user_form, 
        'owner_form': owner_form, 
        'title': 'Press Owner Registration'
    })

# User authentication views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')
