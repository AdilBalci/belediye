from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Vatandaş'),
        ('mayor', 'Belediye Başkanı'),
        ('unit_head', 'Birim Müdürü'),
        ('staff', 'Personel/Mühendis'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_mayor_role(self):
        return self.role == 'mayor'

    @property
    def is_unit_head_role(self):
        return self.role == 'unit_head'

    @property
    def is_staff_role(self):
        return self.role == 'staff'

    @property
    def is_citizen_role(self):
        return self.role == 'citizen'
