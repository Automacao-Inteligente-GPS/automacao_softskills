from django.db import models


class SubSoftSkill(models.Model):
    # campos
    nome = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)
    soft_skill = models.ForeignKey(
        to='capacitacao.SoftSkill', on_delete=models.PROTECT, related_name='soft_skill', null=True
    )
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='sub_soft_skills_cadastradas', null=True
    )
    atualizado_em = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='sub_soft_skills_atualizadas', null=True
    )

    class Meta:
        verbose_name = 'Sub Soft Skill'
        verbose_name_plural = 'Sub Soft Skill'

    def __str__(self):
        return self.nome