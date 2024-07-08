from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from . models import Users
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, get_user_model
from .models import Barbeiro
from django.utils.text import slugify
from django.db.models import Q, Sum
from django.utils.timezone import now, timedelta
from agendamentos.models import Agendamento
from vendas.models import Venda
from dateutil import relativedelta


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('cliente:home'))
        return render(request, 'login.html')
        
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        print(username, senha)
        user = auth.authenticate(username=username, 
                                 password=senha)
        if user:
            auth.login(request, user)
            return redirect(reverse('cliente:home'))
        
        if not user:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos. Tente novamente.')
            return redirect(reverse('usuarios:login'))        
        auth.login(request, user)
        return HttpResponse('Usuário logado com sucesso')

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "As Duas senhas devem ser iguais")
            return redirect(reverse('cadastro'))

        if len(senha) < 3:
            messages.add_message(request, constants.ERROR, "A senha deve ter mais que 6 digitos")
            return redirect(reverse('cadastro'))
        
        users = Users.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usúario com esse ursername")
            return redirect(reverse('cadastro'))
        
        users = Users.objects.create_user(
            username=username,
            email=email,
            password=senha,
            
        )      
        return redirect(reverse('login'))
    
def logout(request):
    request.session.flush()
    return redirect(reverse('usuarios:login'))

def barbeiros(request):
    barbeiros = Barbeiro.objects.all()
    return render(request, 'barbeiros.html', {'barbeiros': barbeiros})




def criar_barbeiro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        bio = request.POST.get('bio')
        especializacao = request.POST.get('especializacao')
        foto = request.FILES.get('foto')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')  # Captura o campo 'email'


        if not all([nome, bio, especializacao, foto, telefone, endereco, email]):
            return render(request, 'criar_barbeiro.html', {'error_message': 'Todos os campos são obrigatórios.'})

        if Barbeiro.objects.filter(nome=nome).exists():
            return render(request, 'criar_barbeiro.html', {'error_message': 'Já existe um barbeiro com esse nome.'})

        nome_slug = slugify(nome)
        i = 1
        username = f"barbeiro_{nome_slug}_{i}"
        while Users.objects.filter(username=username).exists():
            i += 1
            username = f"barbeiro_{nome_slug}_{i}"

        try:
            user = Users.objects.create_user(
                username=username,
                email=email,  # Inclui o email ao criar o usuário
                password='senha_default',  # Você precisa definir uma senha padrão
                cargo='B',  # Cargo de Barbeiro
                telefone=telefone,
                endereco=endereco,
            )
        except Exception as e:
            return render(request, 'criar_barbeiro.html', {'error_message': f'Erro ao criar usuário: {e}'})

        try:
            barbeiro = Barbeiro.objects.create(
                user=user,
                nome=nome,
                bio=bio,
                especializacao=especializacao,
                foto=foto,
            )
            barbeiro.save()
        except Exception as e:
            return render(request, 'criar_barbeiro.html', {'error_message': f'Erro ao criar barbeiro: {e}'})

        return redirect(reverse('usuarios:barbeiros'))

    return render(request, 'criar_barbeiro.html')

# def dashboard_barbeiro(request, barbeiro_id):
#     print("Entrou na view dashboard_barbeiro")  # 1
#     barbeiro = get_object_or_404(Barbeiro, id=barbeiro_id)
#     print("Barbeiro encontrado:", barbeiro)  # 2
#     vendas = Venda.objects.filter(barbeiro=barbeiro)
#     print("Vendas encontradas:", vendas)  # 3

#     periodo = request.GET.get('periodo', 'diario')
#     data_inicio = request.GET.get('data_inicio', None)
#     data_fim = request.GET.get('data_fim', None)

#     vendas_filtradas = filtrar_vendas_por_periodo(vendas, periodo, data_inicio, data_fim)

#     if not vendas_filtradas.exists():
#         print("Nenhum serviço finalizado ainda.")  # 4
#         contexto = {
#             'barbeiro': barbeiro,
#             'mensagem': 'Nenhum serviço finalizado ainda.',
#         }
#     else:
#         print("Vendas filtradas encontradas:", vendas_filtradas)  # 5
#         indicadores = calcular_indicadores_desempenho(vendas_filtradas)
#         print("Indicadores calculados:", indicadores)  # 6
#         contexto = {
#             'barbeiro': barbeiro,
#             'periodo': periodo,
#             'data_inicio': data_inicio,
#             'data_fim': data_fim,
#             'indicadores': indicadores,
#         }

#     print("Contexto criado:", contexto)  # 7
#     response = render(request, 'dashboard_barbeiro.html', contexto)
#     print("Response:", response)  # 8
#     return response


def dashboard_barbeiro(request, barbeiro_id):
    barbeiro = get_object_or_404(Barbeiro, id=barbeiro_id)
    vendas = Venda.objects.filter(barbeiro=barbeiro)

    periodo = request.GET.get('periodo', 'diario')
    data_inicio = request.GET.get('data_inicio', None)
    data_fim = request.GET.get('data_fim', None)

    vendas_filtradas = filtrar_vendas_por_periodo(vendas, periodo, data_inicio, data_fim)

    if not vendas_filtradas.exists():
        contexto = {
            'barbeiro': barbeiro,
            'mensagem': 'Nenhum serviço finalizado ainda.',
        }
    else:
        indicadores = calcular_indicadores_desempenho(vendas_filtradas)
        contexto = {
            'barbeiro': barbeiro,
            'periodo': periodo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'indicadores': indicadores,
        }
    print("Contexto criado:", contexto)
    return render(request, 'dashboard_barbeiro.html', contexto)   

def filtrar_vendas_por_periodo(vendas, periodo, data_inicio, data_fim):
    if periodo == 'diario':
        if data_inicio:
            vendas = vendas.filter(data_hora_venda__date=data_inicio)
        elif data_fim:
            vendas = vendas.filter(data_hora_venda__date__lte=data_fim)
    elif periodo == 'quinzenal':
        if data_inicio:
            data_fim = data_inicio + timedelta(days=14)
            vendas = vendas.filter(data_hora_venda__date__gte=data_inicio, data_hora_venda__date__lte=data_fim)
        elif data_fim:
            data_inicio = data_fim - timedelta(days=14)
            vendas = vendas.filter(data_hora_venda__date__gte=data_inicio, data_hora_venda__date__lte=data_fim)
    elif periodo == 'mensal':
        if data_inicio:
            data_fim = data_inicio + relativedelta.relativedelta(months=+1)
            vendas = vendas.filter(data_hora_venda__date__gte=data_inicio, data_hora_venda__date__lte=data_fim)
        elif data_fim:
            data_inicio = data_fim + relativedelta.relativedelta(months=-1)
            vendas = vendas.filter(data_hora_venda__date__gte=data_inicio, data_hora_venda__date__lte=data_fim)

    return vendas

def calcular_indicadores_desempenho(vendas_filtradas):
    quantidade_vendas = vendas_filtradas.count()
    valor_total_vendas = vendas_filtradas.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    valor_total_comissao = vendas_filtradas.aggregate(Sum('valor_comissao'))['valor_comissao__sum'] or 0
    barbeiro = vendas_filtradas.first().barbeiro if vendas_filtradas.exists() else None
    agendamentos_filtrados = Agendamento.objects.filter(
        barbeiro=barbeiro,
        data_hora_agendamento__date__gte=vendas_filtradas.first().data_hora_venda__date if vendas_filtradas.exists() else None,
        data_hora_agendamento__date__lte=vendas_filtradas.last().data_hora_venda__date if vendas_filtradas.exists() else None,
    ) if barbeiro else Agendamento.objects.none()
    
    quantidade_agendamentos = agendamentos_filtrados.count()
    ticket_medio = valor_total_vendas / (quantidade_vendas or 1)
    taxa_conversao = (quantidade_vendas / (quantidade_agendamentos or 1)) * 100

    indicadores = {
        'quantidade_vendas': quantidade_vendas,
        'valor_total_vendas': valor_total_vendas,
        'valor_total_comissao': valor_total_comissao,
        'ticket_medio': ticket_medio,
        'taxa_conversao': taxa_conversao,
    }

    return indicadores