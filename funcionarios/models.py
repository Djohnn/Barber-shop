from django.db import models
from usuarios.models import Users

class FuncionarioSenha(models.Model):
    funcionario = models.OneToOneField(Users, on_delete=models.CASCADE)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"Senha do funcionário {self.funcionario.username}"