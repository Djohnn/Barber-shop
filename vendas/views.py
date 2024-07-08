from django.shortcuts import render, get_object_or_404, redirect
from .models import Venda, VendaProduto
from agendamentos.models import Agendamento
from estoque.models import Produto
from usuarios.models import Barbeiro

def lista_vendas(request):
    vendas = Venda.objects.filter(status_pagamento='Em Aberto')
    return render(request, 'lista_vendas.html', {'vendas': vendas})

def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'detalhes_venda.html', {'venda': venda})

def criar_venda(request):
    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento')
        produtos_ids = request.POST.getlist('produtos')
        barbeiro_id = request.POST.get('barbeiro')
        desconto = float(request.POST.get('desconto', 0))

        agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
        barbeiro = get_object_or_404(Barbeiro, pk=barbeiro_id)

        venda = Venda.objects.create(
            agendamento=agendamento,
            desconto=desconto,
            barbeiro=barbeiro,
            valor_comissao=0
        )
        for produto_id in produtos_ids:
            produto = get_object_or_404(Produto, pk=produto_id)
            quantidade = int(request.POST.get(f'quantidade_{produto_id}'))
            VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)

        venda.calcular_valor_total()
        return redirect('lista_vendas')

    agendamentos = Agendamento.objects.filter(status='Finalizado')
    produtos = Produto.objects.all()
    barbeiros = Barbeiro.objects.all()
    return render(request, 'criar_venda.html', {'agendamentos': agendamentos, 'produtos': produtos, 'barbeiros': barbeiros})

def aplicar_pagamento_pix(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.status_pagamento = 'Pago'
        venda.save()
        # Atualizar saldo da comissão do barbeiro
        venda.barbeiro.saldo_comissao += venda.valor_comissao
        venda.barbeiro.save()
        return redirect('detalhes_venda', pk=pk)
    return render(request, 'aplicar_pagamento_pix.html', {'venda': venda})

