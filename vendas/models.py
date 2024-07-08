from django.db import models
from usuarios.models import Barbeiro
from estoque.models import Produto
from agendamentos.models import Agendamento
from decimal import Decimal

class Venda(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='VendaProduto')
    desconto = models.FloatField(null=True, blank=True)
    valor_total = models.FloatField()
    data_hora_venda = models.DateTimeField(auto_now_add=True)
    status_pagamento = models.CharField(max_length=20, choices=[('Em Aberto', 'Em Aberto'), ('Pago', 'Pago'), ('Cancelado', 'Cancelado')], default='Em Aberto')
    comprovante_pix = models.CharField(max_length=200, null=True, blank=True)
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    valor_comissao = models.FloatField()
    chave_pix = models.CharField(max_length=100, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=20, choices=[
        ('Dinheiro', 'Dinheiro'),
        ('Cartão Débito', 'Cartão Débito'),
        ('Cartão Crédito', 'Cartão Crédito'),
        ('Pix', 'Pix'),
    ])
    
    def calcular_valor_total(self):
        print("Calculando valor total...")
        total = Decimal('0.00')  # Inicializa o valor total como Decimal
        for vp in self.vendaproduto_set.all():
            produto_total = vp.produto.preco_venda * vp.quantidade
            total += produto_total
            print(f"Adicionando produto: {vp.produto.nome}, Quantidade: {vp.quantidade}, Preço Unitário: {vp.produto.preco_venda}, Total do Produto: {produto_total}")
        
        if self.agendamento.servico:
            total += self.agendamento.servico.preco  # Adiciona o valor do serviço ao valor total
            print(f"Adicionando serviço: {self.agendamento.servico.nome}, Preço: {self.agendamento.servico.preco}")
        
        if self.desconto:
            print(f"Aplicando desconto: {self.desconto}")
            total -= self.desconto
        
        print(f"Valor total calculado: {total}")
        self.valor_total = total  # Atribui o valor total calculado
        self.save()
        print("Valor total salvo no banco de dados")
    # def calcular_valor_total(self):
    #     total = sum([vp.produto.preco_venda * vp.quantidade for vp in self.vendaproduto_set.all()])
    #     if self.desconto:
    #         total -= self.desconto
    #     self.valor_total = total
    #     self.save()

    # def calcular_comissao_barbeiro(self):
    #     comissao_valor = self.valor_total * (self.barbeiro.comissao_porcentagem / 100)
    #     return comissao_valor


        # def calcular_valor_total(self):
    #     total = sum([vp.produto.preco_venda * vp.quantidade for vp in self.vendaproduto_set.all()])
    #     if self.desconto:
    #         total -= self.desconto
    #     self.valor_total = total
    #     self.valor_comissao = total * (self.barbeiro.comissao_porcentagem / 100)
    #     self.save()

class VendaProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
