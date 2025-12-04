from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Account.forms import RegisterForm, LoginForm

def index(request):
    return HttpResponse("Auth")

def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'Account/register.html', {'form' : form})

def signin(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'Account/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return redirect('home')