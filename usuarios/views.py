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
            return redirect(reverse('usuarios:cadastro'))

        if len(senha) < 3:
            messages.add_message(request, constants.ERROR, "A senha deve ter mais que 6 digitos")
            return redirect(reverse('usuarios:cadastro'))
        
        users = Users.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usúario com esse ursername")
            return redirect(reverse('usuarios:cadastro'))
        
        users = Users.objects.create_user(
            username=username,
            email=email,
            password=senha,
            
        )      
        return redirect(reverse('usuarios:login'))
    
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

