from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('sair/', views.logout, name="sair"),
    path('criar_barbeiro/', views.criar_barbeiro, name='criar_barbeiro'),
    path('barbeiros/', views.barbeiros, name='barbeiros'),
    path('dashboard/<int:barbeiro_id>/', views.dashboard_barbeiro, name='dashboard_barbeiro'),
]