# Generated by Django 5.0.6 on 2024-07-06 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agendamentos', '0001_initial'),
        ('servicos', '0001_initial'),
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='barbeiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='usuarios.barbeiro'),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicos.servico'),
        ),
    ]
