# Generated by Django 5.0.6 on 2024-07-08 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='barbeiro',
            name='comissao_porcentagem',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='barbeiro',
            name='saldo_comissao',
            field=models.FloatField(default=0),
        ),
    ]
