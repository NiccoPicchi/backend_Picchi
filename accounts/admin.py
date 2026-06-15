from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']

    # Campi mostrati nella pagina di MODIFICA utente
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informazioni personali', {'fields': ('first_name', 'last_name', 'email')}),
        ('Ruolo e profilo', {'fields': ('role', 'address', 'phone_number')}),
    )

    # Campi mostrati nella pagina di CREAZIONE utente
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name'),
        }),
    )