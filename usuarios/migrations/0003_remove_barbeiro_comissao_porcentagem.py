# Generated by Django 5.0.6 on 2024-07-08 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_barbeiro_comissao_porcentagem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barbeiro',
            name='comissao_porcentagem',
        ),
    ]
