from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):
    family_group = models.ForeignKey('FamilyGroup', on_delete=models.SET_NULL, null=True, blank=True)
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)
    points = models.IntegerField(default=0)
    face_encoding = models.BinaryField(null=True, blank=True)  # Para almacenar el encoding facial
    google_profile_picture = models.URLField(max_length=500, null=True, blank=True)  # URL de la foto de perfil de Google

    def __str__(self):
        return self.username

class FamilyGroup(models.Model):
    name = models.CharField(max_length=100)
    max_members = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Grupo Familiar'
        verbose_name_plural = 'Grupos Familiares'
