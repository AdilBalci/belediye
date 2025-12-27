from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm
from core.ai_service import analyze_complaint_text
import json

@login_required
def complaint_list(request):
    user = request.user
    if user.is_citizen_role:
        complaints = Complaint.objects.filter(owner=user).order_by('-created_at')
    else:
        # Mayor and Staff see all (or filtered by their unit in a real scenario)
        complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})

@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.owner = request.user

            # AI Analysis Trigger
            analysis = analyze_complaint_text(complaint.description)
            complaint.ai_analysis_result = json.dumps(analysis, ensure_ascii=False)

            # Auto-assign if AI suggests a unit (Optional feature, let's just save the suggestion)
            # if analysis.get('suggested_unit'):
            #     complaint.assigned_unit = analysis['suggested_unit']

            complaint.save()
            messages.success(request, 'Şikayetiniz başarıyla oluşturuldu ve yapay zeka tarafından analiz edildi.')
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/create_complaint.html', {'form': form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # Check permission: owner or staff
    if not (request.user == complaint.owner or request.user.is_staff_role or request.user.is_mayor_role or request.user.is_unit_head_role):
        messages.error(request, "Bu şikayeti görüntüleme yetkiniz yok.")
        return redirect('complaint_list')

    ai_data = {}
    if complaint.ai_analysis_result:
        try:
            ai_data = json.loads(complaint.ai_analysis_result)
        except:
            pass

    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint, 'ai_data': ai_data})

@login_required
def assign_complaint(request, pk):
    if not (request.user.is_mayor_role or request.user.is_unit_head_role):
        messages.error(request, "Yetkisiz işlem.")
        return redirect('complaint_list')

    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        unit = request.POST.get('assigned_unit')
        complaint.assigned_unit = unit
        complaint.status = 'assigned'
        complaint.save()
        messages.success(request, f"Şikayet {unit} birimine atandı.")
        return redirect('complaint_detail', pk=pk)

    return redirect('complaint_detail', pk=pk)
