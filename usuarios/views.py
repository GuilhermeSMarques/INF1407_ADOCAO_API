from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistroUsuarioSerializer, UsuarioSerializer


@extend_schema(tags=['Autenticação'])
class RegistroUsuarioView(generics.CreateAPIView):
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Autenticação'], responses=UsuarioSerializer)
class UsuarioAtualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
