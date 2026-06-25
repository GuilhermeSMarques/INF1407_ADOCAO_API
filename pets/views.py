from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from usuarios.models import Usuario

from .models import Pet
from .permissions import PodeGerenciarPet
from .serializers import PetSerializer


@extend_schema(
    tags=['Pets'],
    parameters=[
        OpenApiParameter('especie', str, description='Filtra por especie do pet.'),
        OpenApiParameter('porte', str, description='Filtra por porte do pet.'),
        OpenApiParameter('sexo', str, description='Filtra por sexo do pet.'),
        OpenApiParameter('status', str, description='Filtra por status do pet.'),
        OpenApiParameter('search', str, description='Busca por nome ou raca.'),
    ],
)
class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, PodeGerenciarPet]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Pet.objects.none()

        usuario = self.request.user
        if not usuario.is_authenticated:
            return Pet.objects.none()

        queryset = Pet.objects.select_related('responsavel')

        if usuario.is_staff:
            queryset = queryset.all()
        elif usuario.tipo_usuario == Usuario.TipoUsuario.RESPONSAVEL:
            queryset = queryset.filter(responsavel=usuario)
        else:
            queryset = queryset.filter(status=Pet.Status.DISPONIVEL)

        filtros = {
            'especie': self.request.query_params.get('especie'),
            'porte': self.request.query_params.get('porte'),
            'sexo': self.request.query_params.get('sexo'),
            'status': self.request.query_params.get('status'),
        }

        for campo, valor in filtros.items():
            if valor:
                queryset = queryset.filter(**{campo: valor})

        busca = self.request.query_params.get('search')
        if busca:
            queryset = queryset.filter(nome__icontains=busca) | queryset.filter(raca__icontains=busca)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)
