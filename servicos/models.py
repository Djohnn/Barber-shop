from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='servicos_fotos/')
    comissao_porcentagem = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return self.nome
