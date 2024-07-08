from django.urls import path
from . import views


app_name = "caixa"

urlpatterns = [
    path('', views.caixa_vendas, name='lista_vendas_caixa'),
    path('detalhe/<int:pk>/', views.detalhe_venda, name='detalhe_venda'),
    path('caixa/<int:pk>/', views.caixa, name='caixa'),
    path('gerar_qr_code_pix/<int:pk>/', views.gerar_qr_code_pix, name='gerar_qr_code_pix'),
]
