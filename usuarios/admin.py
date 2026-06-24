from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'nome', 'tipo_usuario', 'is_active', 'is_staff')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff')
    search_fields = ('email', 'nome', 'telefone')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('nome', 'telefone', 'tipo_usuario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined', 'criado_em')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'telefone', 'tipo_usuario', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('criado_em',)
