from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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


class AlterarSenhaSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(write_only=True)
    nova_senha = serializers.CharField(write_only=True, min_length=8)

    def validate_senha_atual(self, value):
        usuario = self.context['request'].user
        if not usuario.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value

    def validate_nova_senha(self, value):
        password_validation.validate_password(value, self.context['request'].user)
        return value

    def save(self, **kwargs):
        usuario = self.context['request'].user
        usuario.set_password(self.validated_data['nova_senha'])
        usuario.save(update_fields=['password'])
        return usuario


class RecuperarSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        usuario = Usuario.objects.filter(email__iexact=email, is_active=True).first()
        resposta = {
            'detail': 'Se o email estiver cadastrado, as instruções de recuperação serão enviadas.',
        }

        if usuario and settings.DEBUG:
            resposta['uid'] = urlsafe_base64_encode(str(usuario.pk).encode())
            resposta['token'] = default_token_generator.make_token(usuario)

        return resposta


class ConfirmarRecuperacaoSenhaSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    nova_senha = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            user_id = force_str(urlsafe_base64_decode(attrs['uid']))
            usuario = Usuario.objects.get(pk=user_id, is_active=True)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            raise serializers.ValidationError({'token': 'Token inválido ou expirado.'})

        if not default_token_generator.check_token(usuario, attrs['token']):
            raise serializers.ValidationError({'token': 'Token inválido ou expirado.'})

        password_validation.validate_password(attrs['nova_senha'], usuario)
        attrs['usuario'] = usuario
        return attrs

    def save(self, **kwargs):
        usuario = self.validated_data['usuario']
        usuario.set_password(self.validated_data['nova_senha'])
        usuario.save(update_fields=['password'])
        return usuario
