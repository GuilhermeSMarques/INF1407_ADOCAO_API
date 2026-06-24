from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()


@extend_schema(
    summary='Verifica se a API está online',
    responses={200: HealthCheckSerializer},
    tags=['Sistema'],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok'})
