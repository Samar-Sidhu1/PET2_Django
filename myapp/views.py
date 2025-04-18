from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Donation
from datetime import datetime
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Get the next parameter or default to home
            next_url = request.GET.get('next', reverse('home'))
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error during signup')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        donation = Donation(
            user=request.user,
            amount=amount,
            date=timezone.now()
        )
        donation.save()
        messages.success(request, f'Thank you for your donation of ₹{amount} on {donation.date.strftime("%Y-%m-%d %H:%M:%S")}')
        return redirect('home')
    return render(request, 'donation_form.html', {'user': request.user})

@login_required
def profile(request):
    user = request.user
    donations = Donation.objects.filter(user=user)  # Get user's donations
    return render(request, 'profile.html', {
        'user': user,
        'donations': donations
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will also delete donations (due to CASCADE)
        logout(request)
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    return redirect('profile')  # GET requests redirect back

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Store the template context before deletion
        context = {
            'user': None,
            'deleted': True,
            'donations': [],
            'total_donations': 0
        }
        
        # Delete the user account
        request.user.delete()
        logout(request)
        
        messages.success(request, 'Your account has been successfully deleted.')
        return render(request, 'profile.html', context)
    
    return redirect('profile')

def pets(request):
    return render(request, 'pets.html')

def about(request):
    return render(request, 'about.html')

def what(request):
    return render(request, 'what.html')