# Generated by Django 4.2.11 on 2024-04-25 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('capacitacao', '0006_autoavaliacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(default=True)),
                ('cadastrado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('cadastrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='soft_skills_cadastradas', to=settings.AUTH_USER_MODEL)),
                ('atualizado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='soft_skills_atualizadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Soft Skill',
                'verbose_name_plural': 'Soft Skills',
            },
        ),
    ]
