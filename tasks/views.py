from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user) | Task.objects.filter(assigned_by=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks.distinct()})
