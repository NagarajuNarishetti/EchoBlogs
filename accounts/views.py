# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from tenants.models import Client, Domain

def home(request):
    """Home page view"""
    return render(request, "home.html")

def register(request):
    """User registration with tenant creation"""
    # Must run only on public schema
    if connection.schema_name != 'public':
        return render(request, "accounts/error.html", {"msg": "Tenant creation must be done from the public schema."})

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "accounts/register.html")

        try:
            # Create user in public schema
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create new tenant
            tenant = Client(schema_name=username.lower(), name=username)
            tenant.save()  # runs migrations for this tenant

            # Create domain for tenant
            domain = Domain()
            domain.domain = f"{username.lower()}.localhost"
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            messages.success(request, f"Account created successfully! Your blog is available at {domain.domain}:8000")
            
            # Auto-login the user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, "accounts/register.html")

    return render(request, "accounts/register.html")

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "accounts/login.html")

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')
