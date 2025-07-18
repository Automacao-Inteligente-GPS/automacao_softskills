from rest_framework import serializers


from capacitacao.models import Discente


class ListDiscenteSerializer(serializers.ModelSerializer):
    mentor_email_ifpb = serializers.SerializerMethodField()
    mentor_email_polo = serializers.SerializerMethodField()
    mentor_nome = serializers.SerializerMethodField()
    projeto_nome = serializers.SerializerMethodField()

    class Meta:
        model = Discente
        fields = (
            'id', 'nome', 'email_academico', 'mentor_email_ifpb', 'mentor_email_polo', 'mentor_nome', 'projeto_nome'
        )

    def get_mentor_email_ifpb(self, obj):
        return getattr(obj, 'mentor_email_ifpb', None)

    def get_mentor_email_polo(self, obj):
        return getattr(obj, 'mentor_email_polo', None)

    def get_mentor_nome(self, obj):
        return getattr(obj, 'mentor_nome', None)

    def get_projeto_nome(self, obj):
        return getattr(obj, 'projeto_nome', None)
