from django.urls import path, include


urlpatterns = [
    path('', include("matches.urls")),
    path('accounts/', include('accounts.urls')),
]