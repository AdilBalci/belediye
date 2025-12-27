from django.db import models
from django.conf import settings

class PermitProject(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Başvuru Yapıldı'),
        ('under_review', 'İncelemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    )

    title = models.CharField(max_length=200, verbose_name="Proje Adı")
    description = models.TextField(verbose_name="Proje Detayı")
    applicant_name = models.CharField(max_length=100, verbose_name="Başvuru Yapan")

    # In a real app, this would be a file upload (PDF/DWG)
    document_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Proje Dosyası Linki")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    assigned_engineer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'staff'},
        related_name='assigned_projects'
    )

    engineer_comments = models.TextField(blank=True, null=True, verbose_name="Mühendis Yorumu")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
