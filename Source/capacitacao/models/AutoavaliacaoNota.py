from django.db import models


class AutoavaliacaoNota(models.Model):
    # campos
    nota = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0)