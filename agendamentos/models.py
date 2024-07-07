from django.db import models
from django.conf import settings
from servicos.models import Servico  # Importando o modelo Servico

STATUS_CHOICES = (
    ('pendente', 'Pendente'),
    ('agendado', 'Agendado'),
    ('finalizado', 'Finalizado'),
)

class Agendamento(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos')
    barbeiro = models.ForeignKey('usuarios.Barbeiro', on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    hora = models.TimeField()
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)  # Alterando para ForeignKey
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.cliente.username} - {self.servico.nome} - {self.data} {self.hora}"
