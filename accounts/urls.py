from django.urls import path, include
from accounts.views import registration, index, signin, logout_view

urlpatterns = [
    path('', registration, name = 'register'),
    path('login/', signin, name = 'login'),
    path('logout/', logout_view, name = 'logout')
]