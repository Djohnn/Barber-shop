from django.urls import path
from . import views


app_name = "caixa"

urlpatterns = [
    path('caixa_aberto/<int:pk>/', views.caixa_aberto, name='caixa_aberto'),
    path('detalhe/<int:caixa_id>/', views.detalhe_caixa, name='detalhe_caixa'),
    path('aplicar_desconto/<int:venda_id>/', views.aplicar_desconto, name='aplicar_desconto'),
    path('registrar_sangria/<int:caixa_id>/', views.sangria, name='registrar_sangria'),
    path('receber_venda/<int:venda_id>/', views.receber_venda, name='receber_venda'),
    path('abrir/', views.abrir_caixa, name='abrir_caixa'),
    path('vendas_diarias/', views.vendas_diarias, name='vendas_diarias'),
    path('detalhes_venda_caixa/<int:venda_id>/', views.detalhes_venda_caixa, name='detalhes_venda_caixa'),
    path('listar_vendas_caixa/', views.listar_vendas_caixa, name='listar_vendas_caixa'),
    path('vendas_fechadas/', views.listar_vendas_fechadas, name='listar_vendas_fechadas'),
    path('caixa/<int:caixa_id>/fechar/', views.fechar_caixa, name='fechar_caixa'),
    path('login_caixa/', views.login_caixa, name='login_caixa'),
]
