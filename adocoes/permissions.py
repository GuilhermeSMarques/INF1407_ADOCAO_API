from rest_framework import permissions

from usuarios.models import Usuario


# Somente adotantes criam solicitações; responsáveis só aprovam/recusam as dos seus pets
class PodeAcessarSolicitacaoAdocao(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.tipo_usuario == Usuario.TipoUsuario.ADOTANTE

        return True

    def has_object_permission(self, request, view, obj):
        usuario = request.user
        if usuario.is_staff:
            return True

        if usuario.tipo_usuario == Usuario.TipoUsuario.RESPONSAVEL:
            return view.action in ['retrieve', 'aprovar', 'recusar'] and obj.pet.responsavel == usuario

        if view.action in ['retrieve', 'destroy']:
            return obj.usuario == usuario

        return False
       

# Favorito só pode ser removido pelo próprio usuário que o criou
class PodeAcessarFavorito(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user