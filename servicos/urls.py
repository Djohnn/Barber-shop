from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('listar_servicos/', views.listar_servicos, name='listar_servicos'),
    path('adicionar_servicos/', views.adicionar_servicos, name='adicionar_servicos'),
     
]
