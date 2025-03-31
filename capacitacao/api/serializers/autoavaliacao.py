from django.db.models import Q, Max
from rest_framework import serializers
import datetime


from capacitacao.models import (
    Autoavaliacao, Discente, Mentor,
    Projeto, DiscenteProjeto, AutoavaliacaoNota,
    SoftSkill, SubSoftSkill
)

PONTOS = {
    'inexistente': 0,
    'inicialmente': 1,
    'parcialmente': 2,
    'adequadamente': 3,
    'totalmente': 4
}

class CreateAutoavaliacaoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    matricula = serializers.CharField(required=False, write_only=True, allow_blank=True)
    curso = serializers.CharField(required=False, write_only=True, allow_blank=True)
    mentor = serializers.CharField(required=True, write_only=True)
    projeto = serializers.CharField(required=True, write_only=True)
    data_entrada = serializers.CharField(required=True, write_only=True)
    observacao = serializers.CharField(required=False, allow_blank=True)
    respostas = serializers.DictField(child=serializers.ListField(), write_only=True)
    respostas_subsoft_skills = serializers.DictField(child=serializers.DictField(child=serializers.ListField()), write_only=True)

    class Meta:
        model = Autoavaliacao
        fields = (
            'id', 'nome', 'email',
            'curso', 'mentor', 'matricula',
            'projeto', 'data_entrada', 'respostas',
            'respostas_subsoft_skills', 'observacao',
        )

    def create(self, validated_data):
        try:
            _usuario_logado = validated_data.pop('usuario_logado')
            _nome = validated_data.pop('nome').lower()
            _email = validated_data.pop('email').lower()
            _matricula = validated_data.pop('matricula') if 'matricula' in validated_data else None
            _curso = validated_data.pop('curso').lower() if 'curso' in validated_data else None
            _mentor = validated_data.pop('mentor').lower()
            _projeto = validated_data.pop('projeto')
            _data_entrada = datetime.datetime.strptime(validated_data.pop('data_entrada'), "%d/%m/%Y").strftime("%Y-%m-%d")
            _respostas = validated_data.pop('respostas')
            _respostas_subsoft_skills = validated_data.pop('respostas_subsoft_skills') if 'respostas_subsoft_skills' in validated_data else None
            _observacao = validated_data.pop('observacao') if 'observacao' in validated_data else None

            _mentor_objeto = Mentor.objects.filter(nome__iexact=_mentor).first()
            _discente_objeto = Discente.objects.filter(matricula=_matricula).first()
            _projeto_objeto = Projeto.objects.filter(nome__iexact=_projeto).first()

            if not _mentor_objeto:
                _mentor_objeto = Mentor.objects.create(
                    nome=_mentor,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado,
                )

            if not _discente_objeto:
                _discente_objeto = Discente.objects.create(
                    nome=_nome,
                    email_academico=_email,
                    matricula=_matricula,
                    curso=_curso,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado,
                )
            else:
                _discente_objeto.nome = _nome
                _discente_objeto.curso = _curso
                _discente_objeto.atualizado_por = _usuario_logado
                _discente_objeto.save()

            if not _projeto_objeto:
                _projeto_objeto = Projeto.objects.create(
                    nome=_projeto,
                    mentor_id=_mentor_objeto.id,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado,
                )
            else:
                _projeto_objeto.mentor_id = _mentor_objeto.id
                _projeto_objeto.atualizado_por = _usuario_logado
                _projeto_objeto.save()

            if not _discente_objeto.discente_projetos.filter(projeto=_projeto_objeto):
                _discente_projeto_objeto = DiscenteProjeto.objects.create(
                    data_entrada=_data_entrada,
                    discente_id=_discente_objeto.id,
                    projeto_id=_projeto_objeto.id,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado,
                )

            _unidade = _discente_objeto.autoavaliacoes.aggregate(Max('unidade'))['unidade__max']
            _autoavaliacao_objeto = Autoavaliacao.objects.create(
                unidade=_unidade + 1 if _unidade else 1,
                observacao=_observacao,
                discente_id=_discente_objeto.id,
                cadastrado_por=_usuario_logado,
                atualizado_por=_usuario_logado,
            )

            for softskill, respostas in _respostas.items():
                nota = 0
                _softskill_objeto = SoftSkill.objects.filter(nome__iexact=softskill.lower()).first()
                if not _softskill_objeto:
                    _softskill_objeto = SoftSkill.objects.create(
                        nome=softskill.lower(),
                        cadastrado_por=_usuario_logado,
                        atualizado_por=_usuario_logado
                    )

                for resposta in respostas:
                    nota += PONTOS.get(resposta.lower(), 0)
                nota = nota / len(respostas)
                AutoavaliacaoNota.objects.create(
                    nota=nota,
                    autoavaliacao_id=_autoavaliacao_objeto.id,
                    soft_skill_id=_softskill_objeto.id,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado
                )

            for softskill, sub_softskills in _respostas_subsoft_skills.items():
                _softskill_objeto = SoftSkill.objects.filter(nome__iexact=softskill.lower()).first()
                notas = []
                if not _softskill_objeto:
                    _softskill_objeto = SoftSkill.objects.create(
                        nome=softskill.lower(),
                        cadastrado_por=_usuario_logado,
                        atualizado_por=_usuario_logado
                    )
                for sub_softskill, respostas in sub_softskills.items():
                    _sub_softskill_objeto = SubSoftSkill.objects.filter(nome__iexact=sub_softskill.lower()).first()
                    nota = 0
                    if not _sub_softskill_objeto:
                        _sub_softskill_objeto = SubSoftSkill.objects.create(
                            nome=sub_softskill.lower(),
                            soft_skill_id=_softskill_objeto.id,
                            cadastrado_por=_usuario_logado,
                            atualizado_por=_usuario_logado
                        )

                    for resposta in respostas:
                        nota += PONTOS.get(resposta.lower(), 0)
                    nota_final = nota / len(respostas)
                    notas.append(nota_final)
                    AutoavaliacaoNota.objects.create(
                        nota=nota_final,
                        autoavaliacao_id=_autoavaliacao_objeto.id,
                        sub_soft_skill_id=_sub_softskill_objeto.id,
                        cadastrado_por=_usuario_logado,
                        atualizado_por=_usuario_logado
                    )

                AutoavaliacaoNota.objects.create(
                    nota=sum(notas)/len(notas),
                    autoavaliacao_id=_autoavaliacao_objeto.id,
                    soft_skill_id=_softskill_objeto.id,
                    cadastrado_por=_usuario_logado,
                    atualizado_por=_usuario_logado
                )

            return _autoavaliacao_objeto
        except:
            return Autoavaliacao.objects.create()


class AutoavaliacaoNotaSerializer(serializers.ModelSerializer):
    softskill = serializers.SerializerMethodField()

    class Meta:
        model = AutoavaliacaoNota
        fields = ['id', 'nota', 'softskill']

    def get_softskill(self, obj):
        if obj.sub_soft_skill:
            return obj.sub_soft_skill.nome
        else:
            return obj.soft_skill.nome


class AutoavaliacaoSerializer(serializers.ModelSerializer):
    notas = serializers.SerializerMethodField()
    notas_sub_softskill = serializers.SerializerMethodField()
    cadastrado_em = serializers.DateTimeField(
        format='%d/%m/%Y',
    )

    class Meta:
        model = Autoavaliacao
        fields = ['id', 'unidade', 'cadastrado_em', 'notas', 'notas_sub_softskill']

    def get_notas(self, obj):
        notas_filtradas = obj.notas.filter(soft_skill__isnull=False)
        return AutoavaliacaoNotaSerializer(notas_filtradas, many=True).data

    def get_notas_sub_softskill(self, obj):
        notas_filtradas = obj.notas.filter(sub_soft_skill__isnull=False)
        return AutoavaliacaoNotaSerializer(notas_filtradas, many=True).data


class ListAutoavaliacaoSerializer(serializers.ModelSerializer):
    data_entrada = serializers.SerializerMethodField()
    autoavaliacoes = AutoavaliacaoSerializer(many=True)

    class Meta:
        model = Discente
        fields = ['id', 'nome', 'autoavaliacoes', 'data_entrada']

    def get_data_entrada(self, obj):
        return obj.discente_projetos.last().data_entrada if obj.discente_projetos.exists() else ''
