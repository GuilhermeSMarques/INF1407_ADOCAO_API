from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Manager customizado para criar usuários usando email como chave primária
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')

        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipo_usuario', Usuario.TipoUsuario.RESPONSAVEL)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Usuário customizado: substitui username por email e adiciona tipo (adotante/responsável)
class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADOTANTE = 'adotante', 'Adotante'
        RESPONSAVEL = 'responsavel', 'Responsável'

    username = None
    email = models.EmailField('email', unique=True)
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ADOTANTE,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self):
        return self.nome or self.email
