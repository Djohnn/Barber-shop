from django.shortcuts import render, redirect, get_object_or_404
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
        comicao = request.POST.get('comicao')

        servico = Servico(nome=nome, preco=preco, foto=foto, comicao=comicao)
        servico.save()
        
        messages.add_message(request, messages.SUCCESS, 'Serviço adicionado com sucesso')
        return redirect(reverse('servicos:listar_servicos'))

    return render(request, 'adicionar_servicos.html')


def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        servico.nome = request.POST.get('nome')
        servico.preco = request.POST.get('preco')
        if 'foto' in request.FILES:
            servico.foto = request.FILES.get('foto')
        servico.comissao_porcentagem = request.POST.get('comissao_porcentagem')
        
        servico.save()
        
        messages.success(request, 'Serviço atualizado com sucesso')
        return redirect(reverse('servicos:listar_servicos'))

    return render(request, 'editar_servico.html', {'servico': servico})

def apagar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    
    if request.method == 'POST':
        servico.delete()
        messages.success(request, 'Serviço apagado com sucesso')
        return redirect(reverse('servicos:listar_servicos'))
    
    return render(request, 'apagar_servico.html', {'servico': servico})