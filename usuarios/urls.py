from django.urls import path

from .views import (
    AlterarSenhaView,
    ConfirmarRecuperacaoSenhaView,
    RecuperarSenhaView,
    RegistroUsuarioView,
    UsuarioAtualView,
)

urlpatterns = [
    path('register/', RegistroUsuarioView.as_view(), name='auth-register'),
    path('me/', UsuarioAtualView.as_view(), name='auth-me'),
    path('change-password/', AlterarSenhaView.as_view(), name='auth-change-password'),
    path('password-reset/', RecuperarSenhaView.as_view(), name='auth-password-reset'),
    path('password-reset/confirm/', ConfirmarRecuperacaoSenhaView.as_view(), name='auth-password-reset-confirm'),
]
