from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.mayor_dashboard, name='mayor_dashboard'),
]
