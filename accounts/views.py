from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import RegistrationForm
from .advanced_password_checker import evaluate_password_strength

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome, {username}! Your account has been created successfully.")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

def home(request):
    return render(request, "home.html")

@csrf_exempt
@require_http_methods(["POST"])
def check_password_api(request):
    try:
        data = json.loads(request.body)
        password = data.get('password', '')
        
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)
        
        result = evaluate_password_strength(password)
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
