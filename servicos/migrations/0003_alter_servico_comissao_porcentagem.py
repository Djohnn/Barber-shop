# Generated by Django 5.0.6 on 2024-07-13 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0002_servico_comissao_porcentagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='comissao_porcentagem',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
