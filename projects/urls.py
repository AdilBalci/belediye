from django.urls import path
from . import views

urlpatterns = [
    path('', views.permit_list, name='permit_list'),
]
