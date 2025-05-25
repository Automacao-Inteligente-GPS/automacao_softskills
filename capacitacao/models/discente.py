from django.db.models import Subquery, OuterRef
from datetime import timedelta
from django.utils import timezone
from django.db import models


class Discente(models.Model):
    # campos
    nome = models.CharField(max_length=100, null=True)
    email_academico = models.EmailField(verbose_name='E-mail Acadêmico', max_length=100, null=True)
    email_polo = models.EmailField(verbose_name='E-mail Polo de Inovação', max_length=100, null=True)
    matricula = models.CharField(verbose_name='Matrícula', max_length=24, null=True)
    curso = models.CharField(max_length=100, null=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='discentes_cadastrados', null=True
    )
    atualizado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='discentes_atualizados', null=True
    )

    class Meta:
        verbose_name = 'Discente'
        verbose_name_plural = 'Discentes'

    def __str__(self):
        return self.nome

    @classmethod
    def aptosCertificacao(cls):
        # avoid circular import
        from capacitacao.models import DiscenteProjeto
        hoje = timezone.now().date()
        aptos = []
        discentes = cls.objects.filter(autoavaliacoes__isnull=False).annotate(
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

        # validação de 1 ano no projeto
        for discente in discentes:
            projetos = discente.discente_projetos.all()

            if not projetos.exists():
                continue
            projeto_mais_recente = projetos.order_by('-data_entrada').first()

            if not projeto_mais_recente.data_entrada:
                continue

            tempo_no_programa = hoje - projeto_mais_recente.data_entrada

            if tempo_no_programa < timedelta(days=365):
                continue

            autoavaliacoes = discente.autoavaliacoes.all().order_by('unidade')

            if not autoavaliacoes.exists():
                continue
            notas_por_soft = {}

            for avaliacao in autoavaliacoes:
                for nota in avaliacao.notas.all():
                    key = nota.soft_skill_id or f"sub-{nota.sub_soft_skill.soft_skill_id}"

                    if key not in notas_por_soft:
                        notas_por_soft[key] = []

                    if nota.sub_soft_skill:
                        notas_por_soft[key].append((nota.sub_soft_skill_id, nota.nota))
                    else:
                        notas_por_soft[key].append(nota.nota)

            # avaliado em soft skills socioemocionais
            softskills_avaliadas = set()

            for key in notas_por_soft.keys():
                if str(key).startswith('sub-'):
                    softskills_avaliadas.add(int(str(key).split('-')[1]))
                else:
                    softskills_avaliadas.add(key)

            if len(softskills_avaliadas) < 3:
                continue

            # nota mínima de 1 em cada softskill
            falhou_nota_minima = False

            for key, notas in notas_por_soft.items():
                if str(key).startswith('sub-'):
                    unidades = {}
                    for sub_id, valor in notas:
                        unidades.setdefault(sub_id, []).append(valor)

                    for media in [sum(v) / len(v) for v in unidades.values()]:
                        if media < 1:
                            falhou_nota_minima = True
                            break
                else:
                    if any(n < 1 for n in notas):
                        falhou_nota_minima = True
                        break

            if falhou_nota_minima:
                continue

            # evolução de dois níveis ou valor máximo
            softskills_ok = 0
            total_softskills = len(softskills_avaliadas)

            for key, notas in notas_por_soft.items():
                if len(notas) < 2:
                    continue

                if str(key).startswith('sub-'):
                    unidade_medias = {}
                    for sub_id, valor in notas:
                        unidade_medias.setdefault(sub_id, []).append(valor)

                    lista_medias = [sum(v) / len(v) for v in unidade_medias.values()]
                else:
                    lista_medias = notas

                lista_medias_ordenada = sorted(lista_medias)

                inicial = lista_medias_ordenada[0]
                restantes = lista_medias_ordenada[1:]

                contador = 0
                for r in restantes:
                    if r >= inicial + 2 or r == 4:
                        contador += 1

                if contador >= round((len(restantes)) * (2 / 3)):
                    softskills_ok += 1

            if softskills_ok >= round(total_softskills * (2 / 3)):
                aptos.append(discente)

        return aptos