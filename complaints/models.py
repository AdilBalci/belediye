from django.db import models
from django.conf import settings

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Beklemede'),
        ('assigned', 'İlgili Birime Atandı'),
        ('resolved', 'Çözüldü'),
        ('rejected', 'Reddedildi'),
    )

    title = models.CharField(max_length=200, verbose_name="Şikayet Başlığı")
    description = models.TextField(verbose_name="Şikayet Detayı")
    image = models.ImageField(upload_to='complaints/', blank=True, null=True, verbose_name="Fotoğraf")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Konum (Opsiyonel)")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    assigned_unit = models.CharField(max_length=100, blank=True, null=True, verbose_name="Atanan Birim")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    ai_analysis_result = models.TextField(blank=True, null=True, verbose_name="Yapay Zeka Analizi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
