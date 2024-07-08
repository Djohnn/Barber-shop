from django.shortcuts import render, get_object_or_404, redirect
from .models import Venda, VendaProduto
from agendamentos.models import Agendamento
from estoque.models import Produto
from usuarios.models import Barbeiro
from django.contrib import messages
from django.urls import reverse
from decimal import Decimal

def lista_vendas(request):
    vendas = Venda.objects.filter(status_pagamento='Em Aberto')
    return render(request, 'lista_vendas.html', {'vendas': vendas})

def detalhes_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'detalhes_venda.html', {'venda': venda})


def criar_venda(request):
    if request.method == 'POST':
        print("Recebendo dados do formulário POST")
        agendamento_id = request.POST.get('agendamento')
        produtos_ids = request.POST.getlist('produtos')
        barbeiro_id = request.POST.get('barbeiro')
        desconto = request.POST.get('desconto', '0')
        forma_pagamento = request.POST.get('forma_pagamento')

        print(f"Agendamento ID: {agendamento_id}")
        print(f"Produtos IDs: {produtos_ids}")
        print(f"Barbeiro ID: {barbeiro_id}")
        print(f"Desconto: {desconto}")
        print(f"Forma de Pagamento: {forma_pagamento}")

        try:
            agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
            print(f"Agendamento: {agendamento}")

            if not desconto:
                desconto = Decimal('0.00')
                print('Desconto não aplicado')
            else:
                desconto = Decimal(desconto)  # Convertendo desconto para Decimal
                print('Desconto aplicado')

            venda, created = Venda.objects.get_or_create(
                agendamento=agendamento,
                defaults={
                    'desconto': desconto,
                    'barbeiro': get_object_or_404(Barbeiro, pk=barbeiro_id),
                    'valor_total': Decimal('0.00'),
                    'forma_pagamento': forma_pagamento
                }
            )

            if not created:
                print("Venda existente encontrada. Atualizando venda existente.")
                venda.desconto = desconto
                venda.forma_pagamento = forma_pagamento
                venda.save()
            else:
                print(f"Nova venda criada: {venda}")

            # Adiciona o valor do serviço ao valor total da venda
            for produto_id in produtos_ids:
                produto = get_object_or_404(Produto, pk=produto_id)
                quantidade = int(request.POST.get(f'quantidade_{produto_id}', 1))
                print(f"Produto: {produto} - Quantidade: {quantidade}")
                VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)
                print(f"Produto adicionado: {produto}, Quantidade: {quantidade}")

            venda.calcular_valor_total()  # Calcula o valor total da venda
            
            print(f"Valor total da venda após cálculo: {venda.valor_total}")

            return redirect(reverse('vendas:lista_vendas'))

        except Exception as e:
            print(f"Erro: {str(e)}")
            messages.error(request, str(e))

    agendamentos = Agendamento.objects.filter(status='pendente')
    if not agendamentos.exists():
        print("Nenhum agendamento pendente encontrado.")
        messages.error(request, 'Nenhum agendamento pendente encontrado.')

    produtos = Produto.objects.all()
    barbeiros = Barbeiro.objects.all()
    return render(request, 'criar_venda.html', {'agendamentos': agendamentos, 'produtos': produtos, 'barbeiros': barbeiros})

# def criar_venda(request):
#     if request.method == 'POST':
#         agendamento_id = request.POST.get('agendamento')
#         produtos_ids = request.POST.getlist('produtos')
#         barbeiro_id = request.POST.get('barbeiro')
#         desconto = request.POST.get('desconto', '0')
#         forma_pagamento = request.POST.get('forma_pagamento')

#         try:
#             agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
#             barbeiro = get_object_or_404(Barbeiro, pk=barbeiro_id)

            
#             if not desconto:
#                 desconto = 0.0
#             else:
#                 desconto = float(desconto)

#             venda = Venda.objects.create(
#                 agendamento=agendamento,
#                 desconto=desconto,
#                 barbeiro=barbeiro,
#                 valor_comissao=0,
#                 forma_pagamento=forma_pagamento
#             )
#             venda.valor_total = 0
            
#             for produto_id in produtos_ids:
#                 produto = get_object_or_404(Produto, pk=produto_id)
#                 quantidade = int(request.POST.get(f'quantidade_{produto_id}'))
#                 VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)
#                 venda.valor_total += produto.preco * quantidade

#             venda.calcular_valor_total()
#             venda.save()
#             return redirect('vendas:vendas')

#         except Exception as e:
#             messages.error(request, str(e))

#     agendamentos = Agendamento.objects.filter(status='pendente')
#     if not agendamentos.exists():
#         messages.error(request, 'Nenhum agendamento pendente encontrado.')

#     produtos = Produto.objects.all()
#     barbeiros = Barbeiro.objects.all()
#     return render(request, 'criar_venda.html', {'agendamentos': agendamentos, 'produtos': produtos, 'barbeiros': barbeiros})

# def criar_venda(request):
#     if request.method == 'POST':
#         agendamento_id = request.POST.get('agendamento')
#         produtos_ids = request.POST.getlist('produtos')
#         barbeiro_id = request.POST.get('barbeiro')
#         desconto = float(request.POST.get('desconto', 0))

#         agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
#         barbeiro = get_object_or_404(Barbeiro, pk=barbeiro_id)

#         venda = Venda.objects.create(
#             agendamento=agendamento,
#             desconto=desconto,
#             barbeiro=barbeiro,
#             valor_comissao=0
#         )
#         for produto_id in produtos_ids:
#             produto = get_object_or_404(Produto, pk=produto_id)
#             quantidade = int(request.POST.get(f'quantidade_{produto_id}'))
#             VendaProduto.objects.create(venda=venda, produto=produto, quantidade=quantidade)

#         venda.calcular_valor_total()
#         return redirect('lista_vendas')

#     agendamentos = Agendamento.objects.filter(status='Pendente')
#     produtos = Produto.objects.all()
#     barbeiros = Barbeiro.objects.all()
#     return render(request, 'criar_venda.html', {'agendamentos': agendamentos, 'produtos': produtos, 'barbeiros': barbeiros})

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

