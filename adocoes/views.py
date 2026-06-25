from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pets.models import Pet
from usuarios.models import Usuario

from .models import SolicitacaoAdocao
from .permissions import PodeAcessarSolicitacaoAdocao
from .serializers import SolicitacaoAdocaoSerializer


@extend_schema(
    tags=['Solicitações'],
    parameters=[
        OpenApiParameter('status', str, description='Filtra por status da solicitação.'),
    ],
)
class SolicitacaoAdocaoViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitacaoAdocaoSerializer
    permission_classes = [IsAuthenticated, PodeAcessarSolicitacaoAdocao]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SolicitacaoAdocao.objects.none()

        usuario = self.request.user
        queryset = SolicitacaoAdocao.objects.select_related('usuario', 'pet', 'pet__responsavel')

        if usuario.is_staff:
            queryset = queryset.all()
        elif usuario.tipo_usuario == Usuario.TipoUsuario.RESPONSAVEL:
            queryset = queryset.filter(pet__responsavel=usuario)
        else:
            queryset = queryset.filter(usuario=usuario)

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def destroy(self, request, *args, **kwargs):
        solicitacao = self.get_object()
        if solicitacao.status != SolicitacaoAdocao.Status.PENDENTE:
            return Response(
                {'detail': 'Somente solicitações pendentes podem ser canceladas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        solicitacao.status = SolicitacaoAdocao.Status.CANCELADA
        solicitacao.save(update_fields=['status', 'atualizado_em'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        solicitacao = self.get_object()
        if solicitacao.status != SolicitacaoAdocao.Status.PENDENTE:
            return Response({'detail': 'A solicitação não está pendente.'}, status=status.HTTP_400_BAD_REQUEST)

        solicitacao.status = SolicitacaoAdocao.Status.APROVADA
        solicitacao.pet.status = Pet.Status.ADOTADO
        solicitacao.pet.save(update_fields=['status', 'atualizado_em'])
        solicitacao.save(update_fields=['status', 'atualizado_em'])
        serializer = self.get_serializer(solicitacao)
        return Response(serializer.data)
    
    @extend_schema(tags=['Favoritos'])
    class FavoritoViewSet(viewsets.ModelViewSet):
        serializer_class = FavoritoSerializer
        permission_classes = [IsAuthenticated, PodeAcessarFavorito]
        http_method_names = ['get', 'post', 'delete', 'head', 'options']

        def get_queryset(self):
            if getattr(self, 'swagger_fake_view', False):
                return Favorito.objects.none()

            return Favorito.objects.select_related('usuario', 'pet').filter(usuario=self.request.user)

        def perform_create(self, serializer):
            serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def recusar(self, request, pk=None):
        solicitacao = self.get_object()
        if solicitacao.status != SolicitacaoAdocao.Status.PENDENTE:
            return Response({'detail': 'A solicitação não está pendente.'}, status=status.HTTP_400_BAD_REQUEST)

        solicitacao.status = SolicitacaoAdocao.Status.RECUSADA
        solicitacao.save(update_fields=['status', 'atualizado_em'])
        serializer = self.get_serializer(solicitacao)
        return Response(serializer.data)