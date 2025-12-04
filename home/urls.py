from django.urls import path, include

from home.views import home

urlpatterns = [
    path('', home, name='home'),
    path('accounts/',include('accounts.urls')),
]