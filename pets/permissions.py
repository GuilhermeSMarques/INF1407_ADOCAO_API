from rest_framework import permissions

from usuarios.models import Usuario


class PodeGerenciarPet(permissions.BasePermission):
    """Permite leitura a qualquer autenticado; escrita apenas a responsáveis e admins."""

    def has_permission(self, request, view):
        # Leitura (GET, HEAD, OPTIONS) é liberada a qualquer usuário autenticado
        if request.method in permissions.SAFE_METHODS:
            return True

        # Criação/edição/exclusão exige perfil de responsável
        return request.user.is_staff or request.user.tipo_usuario == Usuario.TipoUsuario.RESPONSAVEL

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Adotantes só enxergam pets disponíveis; responsáveis veem os próprios
            return request.user.is_staff or obj.responsavel == request.user or obj.status == obj.Status.DISPONIVEL

        # Somente o responsável dono do pet (ou admin) pode alterar
        return request.user.is_staff or obj.responsavel == request.user
