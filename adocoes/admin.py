from django.contrib import admin

from .models import SolicitacaoAdocao


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pet', 'status', 'criado_em', 'atualizado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('usuario__nome', 'usuario__email', 'pet__nome')
    autocomplete_fields = ('usuario', 'pet')
    readonly_fields = ('criado_em', 'atualizado_em')
