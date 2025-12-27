from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'Yapılacak'),
        ('in_progress', 'Devam Ediyor'),
        ('done', 'Tamamlandı'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
