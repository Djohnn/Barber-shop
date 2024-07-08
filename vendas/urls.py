from django.urls import path
from . import views


app_name = "vendas"

urlpatterns = [
    path('', views.lista_vendas, name='lista_vendas'),
    path('detalhes/<int:pk>/', views.detalhes_venda, name='detalhes_venda'),
    path('criar/', views.criar_venda, name='criar_venda'),
    path('pagamento_pix/<int:pk>/', views.aplicar_pagamento_pix, name='aplicar_pagamento_pix'),
]
