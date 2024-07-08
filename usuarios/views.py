from django.shortcuts import render, redirect
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

def dashboard_barbeiro(request, barbeiro_id):
    """
    Gera um dashboard com o desempenho de vendas e comissões do barbeiro especificado.

    Args:
        request: Objeto HttpRequest da requisição.
        barbeiro_id: Chave primária do barbeiro a ser consultado.

    Returns:
        Dicionário com dados do dashboard.
    """

    barbeiro = Barbeiro.objects.get(id=barbeiro_id)
    vendas = Venda.objects.filter(barbeiro=barbeiro)  # Obter vendas do barbeiro

    # Obter parâmetros de filtro de período (da URL ou padrão)
    periodo = request.GET.get('periodo') or 'diario'  # 'diario', 'quinzenal', 'mensal'
    data_inicio = request.GET.get('data_inicio') or None  # Data de início (opcional)
    data_fim = request.GET.get('data_fim') or None  # Data de fim (opcional)

    # Filtrar vendas por período
    vendas_filtradas = filtrar_vendas_por_periodo(vendas, periodo, data_inicio, data_fim)

    # Calcular indicadores de desempenho
    indicadores = calcular_indicadores_desempenho(vendas_filtradas)

    # Contexto do dashboard
    contexto = {
        'barbeiro': barbeiro,
        'periodo': periodo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'indicadores': indicadores,
    }

    return contexto

def filtrar_vendas_por_periodo(vendas, periodo, data_inicio, data_fim):
    """
    Aplica filtros de data nas vendas de acordo com o período selecionado.

    Args:
        vendas: QuerySet de objetos Venda.
        periodo: String indicando o período ('diario', 'quinzenal', 'mensal').
        data_inicio: Data de início do filtro (opcional).
        data_fim: Data de fim do filtro (opcional).

    Returns:
        QuerySet de objetos Venda filtrados.
    """
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
    """
    Calcula os indicadores de desempenho do barbeiro a partir das vendas filtradas.

    Args:
        vendas_filtradas: QuerySet de objetos Venda filtrados por período.

    Returns:
        Dicionário com indicadores de desempenho.
    """

    # Quantidade de vendas
    quantidade_vendas = vendas_filtradas.count()
    valor_total_vendas = vendas_filtradas.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    valor_total_comissao = vendas_filtradas.aggregate(Sum('valor_comissao'))['valor_comissao__sum'] or 0
    agendamentos_filtrados = Agendamento.objects.filter(
        barbeiro=vendas_filtradas[0].barbeiro,  # Assumir que todas as vendas são do mesmo barbeiro
        data_hora_agendamento__date__gte=vendas_filtradas[0].data_hora_venda__date,  # Data de início
        data_hora_agendamento__date__lte=vendas_filtradas[0].data_hora_venda__date,  # Data de fim
    )
    
    quantidade_agendamentos = agendamentos_filtrados.count()
    # Ticket médio (valor total das vendas / quantidade de vendas)
    ticket_medio = valor_total_vendas / (quantidade_vendas or 1)

    # Taxa de conversão (quantidade de vendas / agendamentos)
    taxa_conversao = (quantidade_vendas / quantidade_agendamentos) * 100  # Implementar lógica para calcular a taxa de conversão (necessário acesso aos agendamentos)

    # Indicadores de desempenho
    indicadores = {
        'quantidade_vendas': quantidade_vendas,
        'valor_total_vendas': valor_total_vendas,
        'valor_total_comissao': valor_total_comissao,
        'ticket_medio': ticket_medio,
        'taxa_conversao': taxa_conversao,  # Implementar lógica para calcular
    }

    return indicadores
