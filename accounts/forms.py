from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citizen' # Force citizen role for public signups
        if commit:
            user.save()
        return user
