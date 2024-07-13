# Generated by Django 5.0.6 on 2024-07-13 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0005_remove_vendaproduto_preco_unitario'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendaproduto',
            name='preco_unitario',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
