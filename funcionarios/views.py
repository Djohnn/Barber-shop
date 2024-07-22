from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from .forms import FuncionarioForm, CriarSenhaForm
from usuarios.models import Users
from .models import FuncionarioSenha

def listar_funcionarios(request):
    funcionarios = Users.objects.exclude(cargo='CL')
    return render(request, 'listar_funcionarios.html', {'funcionarios': funcionarios})

def adicionar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            if funcionario.cargo == 'C':  # Caixa
                funcionario.save()
                return redirect(reverse('funcionarios:criar_senha', kwargs={'funcionario_id': funcionario.id}))
            else:
                funcionario.save()
                messages.add_message(request, constants.SUCCESS, 'Funcionário cadastrado com sucesso!')
                return redirect(reverse('funcionarios:listar_funcionarios'))
    else:
        form = FuncionarioForm()
    return render(request, 'adicionar_funcionario.html', {'form': form})

def criar_senha(request, funcionario_id):
    funcionario = Users.objects.get(id=funcionario_id)
    if request.method == 'POST':
        form = CriarSenhaForm(request.POST)
        if form.is_valid():
            senha = form.cleaned_data['senha']
            funcionario.set_password(senha)
            funcionario.save()
            FuncionarioSenha.objects.create(funcionario=funcionario, senha=senha)
            messages.add_message(request, constants.SUCCESS, 'Senha criada com sucesso!')
            return redirect(reverse('funcionarios:listar_funcionarios'))
    else:
        form = CriarSenhaForm()
    return render(request, 'criar_senha.html', {'form': form, 'funcionario': funcionario})