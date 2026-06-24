from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'porte', 'status', 'responsavel', 'criado_em')
    list_filter = ('especie', 'porte', 'status', 'sexo')
    search_fields = ('nome', 'raca', 'responsavel__nome', 'responsavel__email')
    autocomplete_fields = ('responsavel',)
    readonly_fields = ('criado_em', 'atualizado_em')
