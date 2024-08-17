from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import permissions

from capacitacao.api.serializers import ListDiscenteSerializer
from capacitacao.models import Autoavaliacao, Discente, AutoavaliacaoNota


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class DiscenteViewSet(ModelViewSet):
    http_method_names = ['get',]

    def get_serializer_class(self):
        return ListDiscenteSerializer

    def get_queryset(self):
        _queryset = Discente.objects.filter(autoavaliacoes__isnull=False).distinct()

        return _queryset
