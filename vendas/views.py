from django.shortcuts import render, get_object_or_404, redirect
from .models import Venda, VendaProduto
from agendamentos.models import Agendamento
from estoque.models import Produto
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse, reverse_lazy
from decimal import Decimal
from django.http import JsonResponse

def listar_vendas(request):
    vendas = Venda.objects.filter(status_pagamento='Em Aberto').select_related('barbeiro', 'agendamento')
    return render(request, 'listar_vendas.html', {'vendas': vendas})

def listar_vendas_canceladas(request):
    vendas = Venda.objects.filter(status_pagamento='Cancelado').select_related('barbeiro', 'agendamento')
    return render(request, 'listar_vendas_vanceladas.html', {'vendas': vendas})

def reabrir_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if venda.status_pagamento == 'Cancelado':
        venda.status_pagamento = 'Em Aberto'
        venda.save()

        # Reabrir agendamento cancelado
        agendamento = venda.agendamento
        agendamento.status = 'Em Aberto'
        agendamento.save()

        produtos = venda.produtos.all()
        for produto in produtos:
            produto.status = 'Em Aberto'
            produto.save()

    messages.add_message(request, constants.SUCCESS, f'Venda {venda.id} Venda reaberta com sucesso!')
    return redirect(reverse('vendas:listar_vendas'))

def fechar_vendas(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    venda.status_pagamento = 'Fechado'
    venda.save()
    return redirect(reverse_lazy('caixa:vendas_aberta_caixa'))

def cancelar_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    venda.status_pagamento = 'Cancelado'
    venda.save()
    venda.agendamento.cancelar()
    venda.vendaproduto_set.all().delete()
    return redirect(reverse('vendas:listar_vendas'))

def buscar_agendamentos(request):
    agendamentos = Agendamento.objects.select_related('servico').all()
    return render(request, 'buscar_agendamentos.html', {'agendamentos': agendamentos})

def buscar_produtos(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        produtos = Produto.objects.all()
        if nome:
            produtos = produtos.filter(nome__icontains=nome)
        return render(request, 'buscar_produtos.html', {'produtos': produtos})

def adicionar_produto(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade'))
        produto = get_object_or_404(Produto, id=produto_id)
        VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade, preco_unitario=produto.preco_venda)
        venda.valor_total = venda.calcular_valor_total()
        venda.save()
        return redirect(reverse('vendas:detalhe_venda', kwargs={'venda_id': venda_id}))
    produtos = Produto.objects.all()
    messages.add_message(request, constants.SUCCESS, f'Produto {produto.nome} adicionado com sucesso!')
    return render(request, 'adicionar_produto.html', {'venda': venda, 'produtos': produtos})

def gerar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        if forma_pagamento:
            venda.forma_pagamento = forma_pagamento
            venda.status_pagamento = 'Em Aberto'
            venda.valor_total = venda.calcular_valor_total()
            venda.save()
            messages.success(request, 'Venda concluída com sucesso!')
            return redirect(reverse('vendas:listar_vendas'))
    return redirect(reverse('vendas:criar_venda') + f'?venda_id={venda.id}')

def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'detalhes_venda.html', {'venda': venda})

def remover_produto(request, venda_id, venda_produto_id):
    venda = get_object_or_404(Venda, id=venda_id)
    venda_produto = get_object_or_404(VendaProduto, id=venda_produto_id)
    venda_produto.delete()
    venda.valor_total = venda.calcular_valor_total()
    venda.save()
    
    response_data = {
        'message': f'Produto {produto_nome} removido com sucesso!',
        'valor_total': float(venda.valor_total)  # Converte Decimal para float
    }
    return JsonResponse(response_data)

def aplicar_pagamento_pix(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.status_pagamento = 'Pago'
        venda.save()
        venda.barbeiro.saldo_comissao += venda.valor_comissao  # Atualiza saldo da comissão do barbeiro
        venda.barbeiro.save()
        return redirect('detalhes_venda', pk=pk)
    return render(request, 'aplicar_pagamento_pix.html', {'venda': venda})

def criar_ou_obter_venda(agendamento):
    venda, created = Venda.objects.get_or_create(
        agendamento=agendamento,
        defaults={
            'barbeiro': agendamento.barbeiro,
            'valor_total': Decimal('0.00'),
            'status_pagamento': 'Em Aberta'  # Define o status como "Aberta"
        }
    )
    if created:
        venda.valor_total = venda.calcular_valor_total()
        venda.save()
    return venda, created

def criar_venda(request):
    agendamentos = Agendamento.objects.select_related('servico').all()
    produtos = Produto.objects.all()
    formas_pagamento = ['Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'Pix']
    venda = None
    venda_produtos = []
    venda_criada = False

    if request.method == 'POST':
        print("\n### POST request received ###")

        if 'selecionar_agendamento' in request.POST:
            print("Action: Selecionar Agendamento")
            agendamento_id = request.POST.get('agendamento')
            agendamento = get_object_or_404(Agendamento, id=agendamento_id)
            venda, venda_criada = criar_ou_obter_venda(agendamento)
            if venda_criada:
                messages.add_message(request, constants.SUCCESS, 'Venda criada com sucesso!')
            else:
                messages.info(request, 'Venda já existente para este agendamento.')
            print(f"Venda criada: {venda_criada}")

        elif 'adicionar_produto' in request.POST:
            print("Action: Adicionar Produto")
            venda_id = request.POST.get('venda_id')
            venda = get_object_or_404(Venda, id=venda_id)
            produto_id = request.POST.get('produto')
            quantidade = int(request.POST.get('quantidade', 1))
            if produto_id:
                produto = get_object_or_404(Produto, id=produto_id)
                VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade, preco_unitario=produto.preco_venda)
                venda.valor_total = venda.calcular_valor_total()
                venda.save()
                messages.success(request, constants.SUCCESS, f'Produto {produto.nome} adicionado com sucesso.')
            else:
                messages.add_message(request, constants.ERROR, 'Nenhum produto foi selecionado.')

        elif 'concluir_venda' in request.POST:
            print("Action: Concluir Venda")
            venda_id = request.POST.get('venda_id')
            venda = get_object_or_404(Venda, id=venda_id)
            forma_pagamento = request.POST.get('forma_pagamento')
            if forma_pagamento:
                venda.forma_pagamento = forma_pagamento
                venda.status_pagamento = 'Em Aberto'
                venda.valor_total = venda.calcular_valor_total()
                venda.save()
                messages.add_message(request, constants.SUCCESS, 'Venda concluída com sucesso!')
                return redirect(reverse('vendas:listar_vendas'))

    if venda:
        venda_produtos = venda.vendaproduto_set.all()

    print(f"Venda: {venda}")
    print(f"Produtos da Venda: {[vp.produto.nome for vp in venda_produtos]}")

    return render(request, 'criar_venda.html', {
        'agendamentos': agendamentos,
        'produtos': produtos,
        'venda': venda,
        'venda_produtos': venda_produtos,
        'formas_pagamento': formas_pagamento,
        'venda_criada': venda_criada,
        'valor_total': venda.valor_total if venda else Decimal('0.00')
    })

