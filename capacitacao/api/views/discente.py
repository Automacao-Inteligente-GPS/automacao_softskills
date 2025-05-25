from django.db.models import Subquery, OuterRef
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import permissions

from capacitacao.api.serializers import ListDiscenteSerializer
from capacitacao.models import Discente, DiscenteProjeto


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class DiscenteViewSet(ModelViewSet):
    http_method_names = ['get',]

    def get_serializer_class(self):
        return ListDiscenteSerializer

    def get_queryset(self):
        _queryset = Discente.objects.filter(autoavaliacoes__isnull=False).annotate(
            mentor_email_ifpb=Subquery(
                DiscenteProjeto.objects.filter(
                    discente=OuterRef('pk')
                ).order_by('-cadastrado_em').values('projeto__mentor__email_ifpb')[:1]
            ),
            mentor_email_polo=Subquery(
                DiscenteProjeto.objects.filter(
                    discente=OuterRef('pk')
                ).order_by('-cadastrado_em').values('projeto__mentor__email_polo')[:1]
            )
        ).prefetch_related('discente_projetos', 'discente_projetos__projeto', 'discente_projetos__projeto__mentor').distinct()

        return _queryset


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class DiscenteAptosCertificacaoViewSet(ModelViewSet):
    http_method_names = ['get',]

    def get_serializer_class(self):
        return ListDiscenteSerializer

    def get_queryset(self):
        _queryset = Discente.aptosCertificacao()
        return _queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)