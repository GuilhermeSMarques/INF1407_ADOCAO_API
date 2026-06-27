from rest_framework import permissions

from usuarios.models import Usuario


# Leitura é livre para autenticados; escrita e exclusão são restritas ao responsável do pet
class PodeGerenciarPet(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or request.user.tipo_usuario == Usuario.TipoUsuario.RESPONSAVEL

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff or obj.responsavel == request.user or obj.status == obj.Status.DISPONIVEL

        return request.user.is_staff or obj.responsavel == request.user
