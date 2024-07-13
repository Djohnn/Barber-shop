from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    choices_cargo = (
        ('V', 'Vendedor'),
        ('G', 'Gerente'),
        ('C', 'Caixa'),
        ('CL', 'Cliente'),
        ('B', 'Barbeiro')
    )
    cargo = models.CharField(max_length=2, choices=choices_cargo, default='CL')
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)


class Barbeiro(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='barbeiro_profile')
    bio = models.TextField(blank=True)
    especializacao = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to='barbeiros', blank=True)
    nome = models.CharField(max_length=50)
    saldo_comissao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

# class Barbeiro(Users):
#     bio = models.TextField(blank=True)
#     especializacao = models.CharField(max_length=50, blank=True)
#     foto = models.ImageField(upload_to='barbeiros', blank=True)
#     telefone = models.CharField(max_length=20, blank=True)
#     endereco = models.CharField(max_length=255, blank=True)
#     nome = models.CharField(max_length=50) 
   
#     def __str__(self):
#         return self.nome