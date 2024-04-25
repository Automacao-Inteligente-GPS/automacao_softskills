from django.db import models


class Autoavaliacao(models.Model):
    # campos
    unidade = models.DecimalField(max_digits=2, decimal_places=0, null=True, default=1)
    observacao = models.TextField(verbose_name='Observação', null=True, blank=True)
    discente = models.ForeignKey(
        to='capacitacao.Discente', on_delete=models.PROTECT, related_name='autoavaliações',
        null=True
    )
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='autoavaliações_cadastradas',
        null=True
    )
    atualizado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='autoavaliações_atualizadas',
        null=True)

    class Meta:
        verbose_name = 'Autoavaliação'
        verbose_name_plural = 'Autoavaliações'

    def __str__(self):
        return f'A{self.unidade} de {self.discente}'
