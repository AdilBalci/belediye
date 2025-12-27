from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from accounts.models import CustomUser

@login_required
def chat_index(request):
    # List all users to chat with (excluding self)
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})

@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=other_user, content=content)
            return redirect('chat_detail', user_id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')

    return render(request, 'chat/detail.html', {'other_user': other_user, 'chat_messages': messages})
