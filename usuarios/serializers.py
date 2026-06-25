from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'tipo_usuario', 'criado_em', 'is_active']
        read_only_fields = ['id', 'criado_em', 'is_active']


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'telefone', 'tipo_usuario', 'senha']
        read_only_fields = ['id']

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        return Usuario.objects.create_user(password=senha, **validated_data)
