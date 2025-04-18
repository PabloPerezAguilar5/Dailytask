from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FamilyGroup

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'family_group', 'points', 'is_staff')
    list_filter = ('family_group', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('family_group', 'points', 'face_image', 'face_encoding')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('family_group', 'points', 'face_image')}),
    )

@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_members', 'created_at')
    search_fields = ('name',)

admin.site.register(User, CustomUserAdmin)
