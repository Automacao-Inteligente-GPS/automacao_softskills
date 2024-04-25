from django.db import models


class DiscenteProjeto(models.Model):
    VINCULO = (
        ('B', 'Bolsista'),
        ('V', 'Voluntário')
    )

    # campos
    vinculo = models.CharField(verbose_name='Vínculo', max_length=1, choices=VINCULO, null=True)
    data_entrada = models.DateField(verbose_name='Data de Entrada', null=True)
    discente = models.ForeignKey(to='capacitacao.Discente', on_delete=models.PROTECT, related_name='discente_projetos', null=True)
    projeto = models.ForeignKey(to='capacitacao.Projeto', on_delete=models.PROTECT, related_name='discente_projetos', null=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='discente_projetos_cadastrados', null=True)
    atualizado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='discente_projetos_atualizados', null=True)

    class Meta:
        verbose_name = 'Discente Projeto'
        verbose_name_plural = 'Discente Projetos'

    def __str__(self):
        return f'{self.discente} em {self.projeto}'
