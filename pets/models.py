from django.conf import settings
from django.db import models


class Pet(models.Model):
    """Representa um animal disponível para adoção na plataforma."""

    class Especie(models.TextChoices):
        CACHORRO = 'cachorro', 'Cachorro'
        GATO = 'gato', 'Gato'
        OUTRO = 'outro', 'Outro'

    class Sexo(models.TextChoices):
        MACHO = 'macho', 'Macho'
        FEMEA = 'femea', 'Fêmea'
        NAO_INFORMADO = 'nao_informado', 'Não informado'

    class Porte(models.TextChoices):
        PEQUENO = 'pequeno', 'Pequeno'
        MEDIO = 'medio', 'Médio'
        GRANDE = 'grande', 'Grande'

    class Status(models.TextChoices):
        DISPONIVEL = 'disponivel', 'Disponível'
        EM_PROCESSO = 'em_processo', 'Em processo'
        ADOTADO = 'adotado', 'Adotado'
        INDISPONIVEL = 'indisponivel', 'Indisponível'

    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=Especie.choices)
    raca = models.CharField(max_length=100, blank=True)
    # Armazenado em meses para permitir filhotes
    idade = models.PositiveSmallIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=20, choices=Sexo.choices, default=Sexo.NAO_INFORMADO)
    porte = models.CharField(max_length=20, choices=Porte.choices)
    descricao = models.TextField(blank=True)
    foto = models.ImageField(upload_to='pets/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DISPONIVEL)
    # Usuário responsável pelo cadastro do pet (tipo RESPONSAVEL)
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em', 'nome']

    def __str__(self):
        return self.nome
