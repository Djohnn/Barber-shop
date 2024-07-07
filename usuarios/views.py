from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from . models import Users
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, get_user_model
from.models import Barbeiro
from django.utils.text import slugify

# Create your views here.

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


# def criar_barbeiro(request):
#     if request.method == 'POST':
#         # Capturando os dados do formulário POST
#         nome = request.POST.get('nome')
#         bio = request.POST.get('bio')
#         especializacao = request.POST.get('especializacao')
#         foto = request.FILES.get('foto')
#         telefone = request.POST.get('telefone')
#         endereco = request.POST.get('endereco')

#         # Verifica se o campo nome está vazio
#         if not nome:
#             return render(request, 'criar_barbeiro.html', {'error_message': 'O campo Nome é obrigatório.'})

#         # Gerando um nome de usuário único
#         nome_slug = slugify(nome)
#         username = f"barbeiro_{nome_slug}"

#         # Verificando se o nome de usuário já existe
#         if Users.objects.filter(username=username).exists():
#             # Se o nome de usuário já existe, adiciona um número ao final do nome
#             i = 1
#             while Users.objects.filter(username=f"{username}{i}").exists():
#                 i += 1
#             username = f"{username}{i}"

#         user = Users.objects.create_user(
#             username=username,
#             password='senha_default',  # Você precisa definir uma senha padrão
#             cargo='B',  # Cargo de Barbeiro
#             telefone=telefone,
#             endereco=endereco,
#         )

#         # Cria o objeto Barbeiro apenas se o campo nome estiver preenchido
#         barbeiro = Barbeiro.objects.create(
#             user=user,
#             nome=nome,
#             bio=bio,
#             especializacao=especializacao,
#             foto=foto,
#         )
#         barbeiro.save()
#         # Redirecionando após a criação
#         return redirect(reverse('usuarios:barbeiros'))

#     return render(request, 'criar_barbeiro.html')




def criar_barbeiro(request):
    if request.method == 'POST':
        # Capturando os dados do formulário POST
        nome = request.POST.get('nome')
        bio = request.POST.get('bio')
        especializacao = request.POST.get('especializacao')
        foto = request.FILES.get('foto')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')  # Captura o campo 'email'

        # Verifica se todos os campos estão preenchidos
        if not all([nome, bio, especializacao, foto, telefone, endereco, email]):
            return render(request, 'criar_barbeiro.html', {'error_message': 'Todos os campos são obrigatórios.'})

        # Verifica se já existe um barbeiro com o mesmo nome
        if Barbeiro.objects.filter(nome=nome).exists():
            return render(request, 'criar_barbeiro.html', {'error_message': 'Já existe um barbeiro com esse nome.'})

        # Gerando um nome de usuário único
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

        # Redirecionando após a criação
        return redirect(reverse('usuarios:barbeiros'))

    return render(request, 'criar_barbeiro.html')

# import logging

# logger = logging.getLogger(__name__)

# def criar_barbeiro(request):
#     #...
#     try:
#         user = Users.objects.create_user(
#             #...
#         )
#         logger.info(f'Usuário criado com sucesso: {username}')
#     except Exception as e:
#         logger.error(f'Erro ao criar usuário: {e}')
#         return render(request, 'criar_barbeiro.html', {'error_message': f'Erro ao criar usuário: {e}'})

#     try:
#         barbeiro = Barbeiro.objects.create(
#             #...
#         )
#         barbeiro.save()
#         logger.info(f'Barbeiro criado com sucesso: {nome}')
#     except Exception as e:
#         logger.error(f'Erro ao criar barbeiro: {e}')
#         return render(request, 'criar_barbeiro.html', {'error_message': f'Erro ao criar barbeiro: {e}'})

#     # Redirecionando após a criação
#     logger.info(f'Redirecionando para {reverse("usuarios:barbeiros")}')
#     return redirect(reverse('usuarios:barbeiros'))

