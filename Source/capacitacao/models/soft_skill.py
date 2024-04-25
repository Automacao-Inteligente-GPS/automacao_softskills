from django.db import models


class SoftSkill(models.Model):
    #campos
    nome = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='soft_skills_cadastradas', null=True
    )
    atualizado_em = models.ForeignKey(
        to='auth.User', on_delete=models.PROTECT, related_name='soft_skills_atualizadas', null=True
    )

    class Meta:
        verbose_name = 'Soft Skill'
        verbose_name_plural = 'Soft Skills'

    def __str__(self):
        return self.nome
