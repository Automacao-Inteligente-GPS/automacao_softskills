from rest_framework import serializers

from capacitacao.models import Autoavaliacao

class CreateAutoavaliacaoSerializer(serializers.ModelSerializer):
    unidade = serializers.IntegerField(required=True,)

    class Meta:
        model = Autoavaliacao
        fields = ('id', 'unidade',)

    def create(self, validated_data):
        _unidade = validated_data.pop('unidade')
        _autoavaliacao = Autoavaliacao.objects.create(
            unidade=_unidade
        )
        _autoavaliacao.save()

        return _autoavaliacao