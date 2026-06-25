from rest_framework import serializers

from pets.models import Pet

from .models import Favorito, SolicitacaoAdocao


class SolicitacaoAdocaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome', read_only=True)
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)

    class Meta:
        model = SolicitacaoAdocao
        fields = [
            'id',
            'usuario',
            'usuario_nome',
            'pet',
            'pet_nome',
            'mensagem',
            'status',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'usuario', 'usuario_nome', 'pet_nome', 'status', 'criado_em', 'atualizado_em']

    def validate_pet(self, pet):
        if pet.status != Pet.Status.DISPONIVEL:
            raise serializers.ValidationError('Só é possível solicitar adoção de pets disponíveis.')
        return pet

    def validate(self, attrs):
        request = self.context.get('request')
        pet = attrs.get('pet')

        if request and pet:
            existe_pendente = SolicitacaoAdocao.objects.filter(
                usuario=request.user,
                pet=pet,
                status=SolicitacaoAdocao.Status.PENDENTE,
            ).exists()
            if existe_pendente:
                raise serializers.ValidationError('Já existe uma solicitação pendente para este pet.')

        return attrs


class FavoritoSerializer(serializers.ModelSerializer):
    pet_nome = serializers.CharField(source='pet.nome', read_only=True)

    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'pet', 'pet_nome', 'criado_em']
        read_only_fields = ['id', 'usuario', 'pet_nome', 'criado_em']

    def validate(self, attrs):
        request = self.context.get('request')
        pet = attrs.get('pet')

        if request and pet:
            favorito_existe = Favorito.objects.filter(usuario=request.user, pet=pet).exists()
            if favorito_existe:
                raise serializers.ValidationError('Este pet já está nos favoritos.')

        return attrs


class PainelResumoSerializer(serializers.Serializer):
    total_pets = serializers.IntegerField()
    pets_disponiveis = serializers.IntegerField()
    pets_adotados = serializers.IntegerField()
    solicitacoes_pendentes = serializers.IntegerField()
    solicitacoes_aprovadas = serializers.IntegerField()
    solicitacoes_recusadas = serializers.IntegerField()
    favoritos = serializers.IntegerField()
