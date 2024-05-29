from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import permissions

from capacitacao.api.serializers import CreateAutoavaliacaoSerializer
from capacitacao.models import Autoavaliacao


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class AutoavaliacaoViewSet(ModelViewSet):
    http_method_names = ['post',]

    def get_serializer_class(self):
        return CreateAutoavaliacaoSerializer

    def get_queryset(self):
        autoavaliacao = self.request.GET.get('autoavaliacao_id', None)
        _queryset = Autoavaliacao.objects.filter(
            id=autoavaliacao
        ) if autoavaliacao else Autoavaliacao.objects.all()

        return _queryset

    def get_notas(self, autoavaliacao, _response):
        for nota_objeto in autoavaliacao.notas.all():
            _response[nota_objeto.soft_skill.nome] = nota_objeto.nota
        return _response

    def create(self, request, *args, **kwargs):
        _data = request.data
        _serializer = self.get_serializer_class()
        _serializer_data = _serializer(data=_data)

        if _serializer_data.is_valid():
            _autoavaliacao = _serializer_data.save(usuario_logado=request.user)
            _autoavaliacao.cadastrado_por = request.user
            _autoavaliacao.atualizado_por = request.user
            _autoavaliacao.save()
            _serializer_response = _serializer(instance=_autoavaliacao)
            _response = {
                "aluno": _autoavaliacao.discente.nome,
                "autoavaliacao": _autoavaliacao.unidade
            }
            _response = self.get_notas(_autoavaliacao, _response)

            return Response(_response, status=HTTP_201_CREATED)
