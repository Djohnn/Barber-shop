from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('', views.listar_funcionarios, name='listar_funcionarios'),
    path('adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('criar_senha/<int:funcionario_id>/', views.criar_senha, name='criar_senha'),
]
