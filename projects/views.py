from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PermitProject

@login_required
def permit_list(request):
    # In a real app, filtering would be more complex based on role
    projects = PermitProject.objects.all().order_by('-created_at')
    return render(request, 'projects/permit_list.html', {'projects': projects})
