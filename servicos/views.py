from django.shortcuts import render, redirect
from .models import Servico
from django.contrib import messages
from django.urls import reverse

def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'listar_servicos.html', {'servicos': servicos})
# def listar_servicos(request):
#     servicos = Servico.objects.all()
#     return render(request, 'listar_servicos.html', {'servicos': servicos})


def adicionar_servicos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        foto = request.FILES.get('foto')

        servico = Servico(nome=nome, preco=preco, foto=foto)
        servico.save()
        
        messages.add_message(request, messages.SUCCESS, 'Serviço adicionado com sucesso')
        return redirect(reverse('servicos:listar_servicos'))

    return render(request, 'adicionar_servicos.html')


