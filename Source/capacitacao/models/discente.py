from django.db import models


class Discente(models.Model):
    # campos
    nome = models.CharField(max_length=100, null=True)
    email_academico = models.EmailField(verbose_name='E-mail Acadêmico', max_length=100, null=True)
    email_polo = models.EmailField(verbose_name='E-mail Polo de Inovação', max_length=100, null=True)
    matricula = models.CharField(verbose_name='Matrícula', max_length=24, null=True)
    curso = models.CharField(max_length=100, null=True)
    mentor = models.ForeignKey(
        to='capacitacao.Mentor', on_delete=models.PROTECT, related_name='discentes_mentorados', null=True
    )
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
