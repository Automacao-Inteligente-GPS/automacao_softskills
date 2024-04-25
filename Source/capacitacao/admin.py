from django.contrib import admin

from .models import (
    Mentor, Discente, Projeto,
    DiscenteProjeto, Autoavaliacao, SoftSkill)

admin.site.register(Mentor)
admin.site.register(Discente)
admin.site.register(Projeto)
admin.site.register(DiscenteProjeto)
admin.site.register(Autoavaliacao)
admin.site.register(SoftSkill)
