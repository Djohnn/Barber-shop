from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('listar_agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('criar_agendamento/', views.criar_agendamento, name='criar_agendamento'),
    path('editar_agendamento/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    # path('escolher_servico/', views.escolher_servico, name='escolher_servico'),
    path('listar_servicos/', views.escolher_servico, name='listar_servicos'),
    path('agendar_servico/<int:servico_id>/', views.agendar_servico, name='agendar_servico'),
]
