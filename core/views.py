from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint
from projects.models import PermitProject
from tasks.models import Task

def home(request):
    return render(request, 'home.html')

@login_required
def mayor_dashboard(request):
    # Only Mayor can access
    if not request.user.is_mayor_role:
        return render(request, 'home.html') # Or 403

    context = {
        'total_complaints': Complaint.objects.count(),
        'pending_complaints': Complaint.objects.filter(status='pending').count(),
        'total_projects': PermitProject.objects.count(),
        'active_tasks': Task.objects.exclude(status='done').count(),
        'recent_complaints': Complaint.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/mayor_dashboard.html', context)
