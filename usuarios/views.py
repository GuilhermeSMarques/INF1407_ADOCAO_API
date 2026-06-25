from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AlterarSenhaSerializer,
    ConfirmarRecuperacaoSenhaSerializer,
    RecuperarSenhaSerializer,
    RegistroUsuarioSerializer,
    UsuarioSerializer,
)


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


@extend_schema(tags=['Autenticação'], request=AlterarSenhaSerializer)
class AlterarSenhaView(generics.GenericAPIView):
    serializer_class = AlterarSenhaSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Senha alterada com sucesso.'})


@extend_schema(tags=['Autenticação'], request=RecuperarSenhaSerializer)
class RecuperarSenhaView(generics.GenericAPIView):
    serializer_class = RecuperarSenhaSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save())


@extend_schema(tags=['Autenticação'], request=ConfirmarRecuperacaoSenhaSerializer)
class ConfirmarRecuperacaoSenhaView(generics.GenericAPIView):
    serializer_class = ConfirmarRecuperacaoSenhaSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Senha redefinida com sucesso.'}, status=status.HTTP_200_OK)
