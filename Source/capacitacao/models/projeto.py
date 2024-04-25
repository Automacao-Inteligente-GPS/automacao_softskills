from django.db import models


class Projeto(models.Model):
    TIPO = (
        ('R', 'Real'),
        ('E', 'Espelho'),
    )

    # campos
    nome = models.CharField(max_length=100, null=True)
    tipo = models.CharField(verbose_name='Tipo do Projeto', max_length=1, choices=TIPO, null=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    autalizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='projetos_cadastrados',
                                       null=True)
    atualizado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='projetos_atualizados',
                                       null=True)

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return self.nome
