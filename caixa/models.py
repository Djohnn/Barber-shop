from django.db.models import Sum
from django.db import models
from vendas.models import Venda  # Importe o modelo Venda

class Caixa(models.Model):
    # ...
    valor_abertura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Valor inicial do caixa
    valor_fechamento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Valor final do caixa

    def fechar_caixa(self, valor_fechamento_usuario):
        if self.status:  # Verifica se o caixa está aberto
            vendas_finalizadas = Venda.objects.filter(status_pagamento='Pago', data_hora_venda__date=datetime.now().date())
            valor_vendas_finalizadas = vendas_finalizadas.aggregate(total=Sum('valor_total'))['total'] or 0

            if valor_vendas_finalizadas == valor_fechamento_usuario:
                self.horario_fechamento = datetime.now()
                self.status = False
                self.valor_fechamento = valor_vendas_finalizadas
                self.save()
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return f"Caixa aberto por {self.usuario} em {self.horario_abertura}"