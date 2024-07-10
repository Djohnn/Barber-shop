from django.shortcuts import render, get_object_or_404, redirect
from .models import Venda, VendaProduto
from agendamentos.models import Agendamento
from estoque.models import Produto
from usuarios.models import Barbeiro
from django.contrib import messages
from django.urls import reverse
from decimal import Decimal
from django.http import JsonResponse



def lista_vendas(request):
    vendas = Venda.objects.filter(status_pagamento='Em Aberto')
    return render(request, 'lista_vendas.html', {'vendas': vendas})


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
        VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)
        venda.valor_total = venda.calcular_valor_total()
        venda.save()
        return redirect(reverse('vendas:detalhe_venda', venda_id=venda_id))
    produtos = Produto.objects.all()
    return render(request, 'adicionar_produto.html', {'venda': venda, 'produtos': produtos})

def gerar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        venda.forma_pagamento = forma_pagamento
        venda.status_pagamento = 'Pago'
        venda.save()
        return redirect(reverse('vendas:lista_vendas'))
    formas_pagamento = ['Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'Pix']
    return render(request, 'gerar_venda.html', {'venda': venda, 'formas_pagamento': formas_pagamento})

def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'detalhes_venda.html', {'venda': venda})

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


def criar_venda(request):
    agendamentos = Agendamento.objects.select_related('servico').all()
    produtos = Produto.objects.all()
    formas_pagamento = ['Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'Pix']
    venda = None
    venda_produtos = []

    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento')
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade', 1))
        forma_pagamento = request.POST.get('forma_pagamento')

        print(f"Agendamento ID: {agendamento_id}")
        print(f"Produto ID: {produto_id}")
        print(f"Quantidade: {quantidade}")
        print(f"Forma de Pagamento: {forma_pagamento}")

        if agendamento_id:
            agendamento = get_object_or_404(Agendamento, id=agendamento_id)
            venda, created = Venda.objects.get_or_create(
                agendamento=agendamento,
                defaults={'barbeiro': agendamento.barbeiro, 'valor_total': Decimal('0.00')}
            )
            print(f"Venda criada: {created}")

        if produto_id and venda:
            produto = get_object_or_404(Produto, id=produto_id)
            venda_produto = VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)
            venda_produtos.append(venda_produto)
            venda.valor_total = venda.calcular_valor_total()
            venda.save()
            print(f"Produto adicionado: {produto.nome}, Quantidade: {quantidade}")
            print(f"Valor total da venda: {venda.valor_total}")

        if forma_pagamento and venda:
            venda.forma_pagamento = forma_pagamento
            venda.status_pagamento = 'Pago'
            venda.valor_total = venda.calcular_valor_total()
            venda.save()
            print(f"Venda concluída com forma de pagamento: {forma_pagamento}")
            return redirect(reverse('vendas:lista_vendas'))

    if venda:
        venda_produtos = venda.vendaproduto_set.all()

    return render(request, 'criar_venda.html', {
        'agendamentos': agendamentos,
        'produtos': produtos,
        'venda': venda,
        'venda_produtos': venda_produtos,
        'formas_pagamento': formas_pagamento,
    })




# def criar_venda(request):
#     agendamentos = Agendamento.objects.select_related('servico').all()
#     produtos = Produto.objects.all()
#     formas_pagamento = ['Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'Pix']
#     venda = None
#     venda_produtos = []

#     if request.method == 'POST':
#         agendamento_id = request.POST.get('agendamento')
#         produto_id = request.POST.get('produto')
#         quantidade = int(request.POST.get('quantidade', 1))
#         forma_pagamento = request.POST.get('forma_pagamento')

#         if agendamento_id:
#             agendamento = get_object_or_404(Agendamento, id=agendamento_id)
#             venda, created = Venda.objects.get_or_create(
#                 agendamento=agendamento,
#                 defaults={'barbeiro': agendamento.barbeiro, 'valor_total': Decimal('0.00')}
#             )

#         if produto_id and venda:
#             produto = get_object_or_404(Produto, id=produto_id)
#             venda_produto = VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)
#             venda_produtos.append(venda_produto)
#             venda.valor_total = venda.calcular_valor_total()
#             venda.save()

#         if forma_pagamento and venda:
#             venda.forma_pagamento = forma_pagamento
#             venda.status_pagamento = 'Pago'
#             venda.valor_total = venda.calcular_valor_total()
#             venda.save()
#             return redirect(reverse('vendas:lista_vendas'))

#     if venda:
#         venda_produtos = venda.vendaproduto_set.all()

#     return render(request, 'criar_venda.html', {
#         'agendamentos': agendamentos,
#         'produtos': produtos,
#         'venda': venda,
#         'venda_produtos': venda_produtos,
#         'formas_pagamento': formas_pagamento,
#     })
