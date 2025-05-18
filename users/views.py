from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('users:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('users:signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        print("CREATED")
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('users:signin')

    return render(request, 'users/signup.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('books:home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('users:signin')

    return render(request, 'users/signin.html')


def signout(request):
    logout(request)
    return redirect('users:signin')


def auth(request):
    return render(request, 'users/auth.html')