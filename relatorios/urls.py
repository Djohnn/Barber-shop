from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('vendas/', views.relatorio_vendas, name='relatorio_vendas'),
    path('caixa/', views.relatorio_caixa, name='relatorio_caixa'),
    path('comissoes/', views.relatorio_comissoes, name='relatorio_comissoes'),
]
