from django.db import models


class AutoavaliacaoNota(models.Model):
    # campos
    nota = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0)
    autoavaliacao = models.ForeignKey(
        to='capacitacao.Autoavaliacao', on_delete=models.PROTECT, related_name='notas', null=True
    )
    soft_skill = models.ForeignKey(
        to='capacitacao.SoftSkill', on_delete=models.PROTECT, related_name='notas', null=True, blank=True
    )
    sub_soft_skill = models.ForeignKey(
        to='capacitacao.SubSoftSkill', on_delete=models.PROTECT, related_name='notas', null=True, blank=True
    )
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='notas_cadastradas', null=True
    )
    atualizado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='notas_atualizadas', null=True
    )

    class Meta:
        verbose_name = 'Nota da Autoavaliação'
        verbose_name_plural = 'Notas das Autoavaliações'

    def __str__(self):
        return (f'{self.autoavaliacao.discente}: {self.nota} - '
                + (str(self.sub_soft_skill) if self.sub_soft_skill else str(self.soft_skill)))
