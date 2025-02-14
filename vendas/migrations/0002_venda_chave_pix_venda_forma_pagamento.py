# Generated by Django 5.0.6 on 2024-07-08 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='chave_pix',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='forma_pagamento',
            field=models.CharField(choices=[('Dinheiro', 'Dinheiro'), ('Cartão Débito', 'Cartão Débito'), ('Cartão Crédito', 'Cartão Crédito'), ('Pix', 'Pix')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
