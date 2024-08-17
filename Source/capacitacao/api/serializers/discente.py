from rest_framework import serializers


from capacitacao.models import (
    Autoavaliacao, Discente, Mentor,
    Projeto, DiscenteProjeto, AutoavaliacaoNota,
    SoftSkill
)


class ListDiscenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discente
        fields = (
            'id', 'nome', 'email_academico',
        )
