from django.urls import path

from .views import RegistroUsuarioView, UsuarioAtualView

urlpatterns = [
    path('register/', RegistroUsuarioView.as_view(), name='auth-register'),
    path('me/', UsuarioAtualView.as_view(), name='auth-me'),
]
