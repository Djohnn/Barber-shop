# Generated by Django 5.0.6 on 2024-07-08 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='comissao_porcentagem',
            field=models.FloatField(default=0),
        ),
    ]
