from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('listar_servicos/', views.listar_servicos, name='listar_servicos'),
    path('adicionar_servicos/', views.adicionar_servicos, name='adicionar_servicos'),
    path('editar_servico/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('apagar_servico/<int:servico_id>/', views.apagar_servico, name='apagar_servico'),
     
]
