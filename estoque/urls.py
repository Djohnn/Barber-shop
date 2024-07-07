from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('add_produto/', views.add_produto, name='add_produto'),
    path('produto/<slug:slug>', views.produto, name="produto"),
    path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    # path('editar_produto/<int:produto_id>/', views.editar_produto, name='editar_produto'),

]