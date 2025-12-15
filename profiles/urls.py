from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='view'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),   
]