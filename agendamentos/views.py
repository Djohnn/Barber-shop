from django.shortcuts import render, get_object_or_404, redirect
#TODO ATIVAR AS PROTEÇÃO DAS VIEWS
#from django.contrib.auth.decorators import login_required
from .models import Agendamento
from .forms import AgendamentoForm
from servicos.models import Servico
from usuarios.models import Barbeiro
from django.contrib import messages
from django.urls import reverse

# @login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'listar_agendamentos.html', {'agendamentos': agendamentos})

# @login_required
def criar_agendamento(request):
    servicos = Servico.objects.all()
    barbeiros = Barbeiro.objects.all()
    servico_id = request.GET.get('servico')
    servico_selecionado = None

    if servico_id:
        servico_selecionado = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        servico = get_object_or_404(Servico, id=request.POST.get('servico'))
        barbeiro = get_object_or_404(Barbeiro, id=request.POST.get('barbeiro'))

        Agendamento.objects.create(
            cliente=request.user,
            barbeiro=barbeiro,
            data=data,
            hora=hora,
            servico=servico,
            status='Pendente'
        )
        servico.status = 'agendado'
        servico.save()
        return redirect('cliente:home')

    return render(request, 'criar_agendamento.html', {
        'servicos': servicos,
        'barbeiros': barbeiros,
        'servico_selecionado': servico_selecionado,
    })

# @login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    servicos = Servico.objects.all()
    barbeiros = Barbeiro.objects.all()

    if request.method == 'POST':
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        servico_id = request.POST.get('servico')
        barbeiro_id = request.POST.get('barbeiro')
       

        servico = get_object_or_404(Servico, id=servico_id)
        barbeiro = get_object_or_404(Barbeiro, id=barbeiro_id)

        agendamento.data = data
        agendamento.hora = hora
        agendamento.servico = servico
        agendamento.barbeiro = barbeiro
        servico.status = 'agendado'
        servico.save()
        agendamento.save()

        return redirect(reverse('agendamentos:listar_agendamentos'))

    return render(request, 'editar_agendamento.html', {
        'agendamento': agendamento,
        'servicos': servicos,
        'barbeiros': barbeiros,
    })


#@login_required
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'listar_serviços.html', {'servicos': servicos})



def escolher_servico(request):
    servicos = Servico.objects.all()
    return render(request, 'escolher_servico.html', {'servicos': servicos})

def agendar_servico(request):
    if request.metohd == 'GET':
        servicos = Servico.objects.all()
        barbeiros = Barbeiro.objects.all()
        servico_id = request.GET.get('servico')
        servico_selecionado = None

        if servico_id:
            servico_selecionado = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        servico = get_object_or_404(Servico, id=request.POST.get('servico'))
        barbeiro = get_object_or_404(Barbeiro, id=request.POST.get('barbeiro'))

        Agendamento.objects.create(
            cliente=request.user,
            barbeiro=barbeiro,
            data=data,
            hora=hora,
            servico=servico,
            status='Pendente'
        )
        servico._status = 'agendado'
        servico.save()
        messages.success(request, 'Agendamento criado com sucesso!')
        return redirect(reverse('listar_agendamentos'))

    return render(request, 'criar_agendamento.html', {
        'servicos': servicos,
        'barbeiros': barbeiros,
        'servico_selecionado': servico_selecionado,
    })
