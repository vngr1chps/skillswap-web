from django.urls import path, include

from home.views import home

urlpatterns = [
    path('', include("matches.urls")),
    path('accounts/', include('accounts.urls')),
]