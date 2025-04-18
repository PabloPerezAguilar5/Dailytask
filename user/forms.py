from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FamilyGroup

class UserRegistrationForm(UserCreationForm):
    face_image = forms.ImageField(required=True)
    family_group = forms.ModelChoiceField(
        queryset=FamilyGroup.objects.all(),
        required=False,
        empty_label="Seleccionar grupo familiar"
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'face_image', 'family_group') 