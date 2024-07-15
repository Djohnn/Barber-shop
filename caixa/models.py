from django.db import models
from usuarios.models import Users
from vendas.models import Venda
from django.utils import timezone



class Caixa(models.Model):
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    aberto = models.BooleanField(default=True)
    funcionario = models.ForeignKey(Users, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.aberto:
            self.data_fechamento = None  # Se o caixa está aberto, não deve haver data de fechamento
        else:
            self.data_fechamento = timezone.now()  # Define a data de fechamento ao fechar o caixa

        super().save(*args, **kwargs)


    def atualizar_valor_total(self, venda_id):
        venda = Venda.objects.get(id=venda_id)
        if self.aberto and venda.status_pagamento == 'Pago':
            self.valor_total += venda.valor_total
            self.save()
        else:
            print("Erro: caixa não está aberto ou venda não está paga")

    def fechar_caixa(self, valor_fechamento):
        if not self.aberto:
            raise ValueError("Caixa não está aberto")

        valor_total_caixa = self.valor_total
        valor_fechamento_float = float(valor_fechamento)
        if round(valor_fechamento_float, 2)!= round(valor_total_caixa, 2):
            raise ValueError("Valor de fechamento não coincide com o valor total do caixa")

        self.aberto = False
        self.data_fechamento = timezone.now()
        self.save()


    def __str__(self):
        status = 'Aberto' if self.aberto else 'Fechado'
        return f"Caixa {self.id} - {self.funcionario.username} - {status}"


class Sangria(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()

    def __str__(self):
        return f"Sangria {self.id} - Caixa {self.caixa.id} - Valor {self.valor}"

class Desconto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=[
        ('Serviço', 'Serviço'),
        ('Produto', 'Produto'),
        ('Total', 'Total')
    ])

    def __str__(self):
        return f"Desconto {self.id} - Venda {self.venda.id} - {self.tipo} - Valor {self.valor}"


    # def fechar_caixa(self, valor_fechamento_usuario):
    #     if self.status:  # Verifica se o caixa está aberto
    #         vendas_finalizadas = Venda.objects.filter(status_pagamento='Pago', data_hora_venda__date=datetime.now().date())
    #         valor_vendas_finalizadas = vendas_finalizadas.aggregate(total=Sum('valor_total'))['total'] or 0

    #         if valor_vendas_finalizadas == valor_fechamento_usuario:
    #             self.horario_fechamento = datetime.now()
    #             self.status = False
    #             self.valor_fechamento = valor_vendas_finalizadas
    #             self.save()
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    # def __str__(self):
    #     return f"Caixa aberto por {self.usuario} em {self.horario_abertura}"