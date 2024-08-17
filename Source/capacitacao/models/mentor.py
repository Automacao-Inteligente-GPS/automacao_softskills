from django.db import models


class Mentor(models.Model):
    TIPO = (
        ('T', 'Técnico'),
        ('S', 'Soft Skills'),
        ('P', 'PBL')
    )

    nome = models.CharField(max_length=100, null=True)
    tipo = models.CharField(verbose_name='Tipo do Mentor', max_length=1, choices=TIPO, null=True)
    email_ifpb = models.EmailField(verbose_name='E-mail Ifpb', max_length=100, null=True)
    email_polo = models.EmailField(verbose_name='E-mail Polo de Inovação', max_length=100, null=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    cadastrado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='mentores_cadastrados',
                                       null=True)
    atualizado_por = models.ForeignKey(to='auth.User', on_delete=models.PROTECT, related_name='mentores_atualizados',
                                       null=True)

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentores'

    def __str__(self):
        return self.nome
