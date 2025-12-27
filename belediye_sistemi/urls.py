from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('complaints/', include('complaints.urls')),
    path('projects/', include('projects.urls')),
    path('chat/', include('chat.urls')),
    path('tasks/', include('tasks.urls')),
    path('mayor/', include('core.urls')), # For mayor dashboard specific views if any
]
