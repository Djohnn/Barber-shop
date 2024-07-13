from django.urls import path
from . import views


app_name = "vendas"

urlpatterns = [
    path('', views.listar_vendas, name='listar_vendas'),
    path('detalhes/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    path('criar/', views.criar_venda, name='criar_venda'),
    path('pagamento_pix/<int:pk>/', views.aplicar_pagamento_pix, name='aplicar_pagamento_pix'),
    path('buscar_produtos/', views.buscar_produtos, name='buscar_produtos'),
    path('buscar_agendamentos/', views.buscar_agendamentos, name='buscar_agendamentos'),
    path('adicionar_produto/<int:venda_id>/', views.adicionar_produto, name='adicionar_produto'),
    path('gerar_venda/<int:venda_id>/', views.gerar_venda, name='gerar_venda'),
    path('remover_produto/<int:venda_id>/<int:venda_produto_id>/', views.remover_produto, name='remover_produto'),
    path('vendas/<pk>/fechar_venda/', views.fechar_vendas, name='fechar_venda'),
    path('vendas/<pk>/cancelar_venda/', views.cancelar_venda, name='cancelar_venda'),
    path('canceladas/', views.listar_vendas_canceladas, name='listar_vendas_cancelada'),
    path('reabrir/<pk>/', views.reabrir_venda, name='reabrir_venda'),

]
