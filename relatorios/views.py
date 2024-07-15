from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from caixa.models import Caixa
# from vendas.models import Venda
from django.utils.timezone import now
from datetime import timedelta

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
