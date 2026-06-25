from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id',
            'nome',
            'especie',
            'raca',
            'idade',
            'sexo',
            'porte',
            'descricao',
            'foto',
            'status',
            'responsavel',
            'responsavel_nome',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'responsavel', 'responsavel_nome', 'criado_em', 'atualizado_em']
