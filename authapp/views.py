from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# Register
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'authapp/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
    else:
        form = LoginForm()
    return render(request, 'authapp/login.html', {'form': form})


def home(request):
    return render(request, 'authapp/home.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('customer_dashboard')
    return render(request, 'authapp/admin_dashboard.html')

# Customer Dashboard
@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('admin_dashboard')
    return render(request, 'authapp/customer_dashboard.html')
