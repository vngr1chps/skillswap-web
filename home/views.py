from django.http import HttpResponse
from django.shortcuts import render

menu = [
    'profile',
    'likes'
]

def home(request):
    return render(request, 'Home/home.html', {'menu': menu})
