from django.conf import settings
from django.db import models

from pets.models import Pet


class SolicitacaoAdocao(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        APROVADA = 'aprovada', 'Aprovada'
        RECUSADA = 'recusada', 'Recusada'
        CANCELADA = 'cancelada', 'Cancelada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitacoes_adocao',
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='solicitacoes')
    mensagem = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'pet'],
                condition=models.Q(status='pendente'),
                name='solicitacao_pendente_unica_por_usuario_pet',
            ),
        ]

    def __str__(self):
        return f'{self.usuario} - {self.pet}'
