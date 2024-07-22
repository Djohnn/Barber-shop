from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from caixa.models import Caixa
from django.utils.timezone import now
from datetime import timedelta
from agendamentos.models import Agendamento
from usuarios.models import Barbeiro
from vendas.models import Venda
from django.db.models import Q, Sum
from django.utils.timezone import now, timedelta
from dateutil import relativedelta


@login_required
def relatorio_vendas(request):
    vendas = Venda.objects.filter(data_hora_venda__date=now().date())
    return render(request, 'relatorios/relatorio_vendas.html', {'vendas': vendas})

@login_required
def relatorio_caixa(request):
    caixas_abertos = Caixa.objects.filter(aberto=True)
    return render(request, 'relatorios/relatorio_caixa.html', {'caixas_abertos': caixas_abertos})

@login_required
def relatorio_comissoes(request):
    comissoes = Venda.objects.filter(status_pagamento='Pago').values('barbeiro__nome').annotate(total_comissao=Sum('valor_comissao'))
    return render(request, 'relatorios/relatorio_comissoes.html', {'comissoes': comissoes})

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