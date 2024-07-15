from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .models import Caixa, Desconto, Sangria
from django.contrib.messages import constants
from django. contrib import messages
from .decorators import caixa_aberto_required
from cliente.views import Agendamento
from vendas.models import VendaProduto, Venda
from django.utils import timezone
from usuarios.models import Users
from decimal import Decimal


@login_required
def listar_vendas_fechadas(request):
    vendas_fechadas = Venda.objects.filter(status_pagamento='Fechada').order_by('-data_hora_venda').select_related('barbeiro', 'agendamento')
    return render(request, 'listar_vendas_fechadas.html', {'vendas_fechadas': vendas_fechadas})


@login_required
def listar_vendas_caixa(request):
    vendas = Venda.objects.filter(status_pagamento='Fechada').order_by('-data_hora_venda')
    return render(request, 'listar_vendas_caixa.html', {'caixa': vendas})


@login_required
def abrir_caixa(request):
    if request.method == 'POST':
        valor_inicial = request.POST.get('valor_inicial')
        caixa = Caixa.objects.create(funcionario=request.user, valor_inicial=valor_inicial)
        messages.add_message(request, constants.SUCCESS, 'Caixa aberto com sucesso!')
        return redirect('caixa:detalhe_caixa', caixa_id=caixa.id)
    return render(request, 'abrir_caixa.html')

@login_required
@login_required
def caixa_aberto(request, pk):
    caixa = get_object_or_404(Caixa, pk=pk)
    vendas = Venda.objects.filter(status_pagamento='Pago', data_hora_venda__gte=caixa.data_abertura)
    caixa.atualizar_valor_total()
    return render(request, 'caixa_aberto.html', {'caixa': caixa, 'vendas': vendas})

@login_required
@caixa_aberto_required
@login_required
def fechar_caixa(request, caixa_id):
    print("Entrou na função fechar_caixa")
    print("Request method:", request.method)
    print("Caixa ID:", caixa_id)
    
    caixa = Caixa.objects.get(id=caixa_id)
    print("Caixa:", caixa)
    
    if request.method == 'POST':
        print("Request é POST")
        caixa = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
        print("Caixa aberto:", caixa)
        
        if not caixa:
            print("Nenhum caixa aberto encontrado")
            messages.add_message(request, constants.ERROR, "Nenhum caixa aberto encontrado.")
            return redirect(reverse('caixa:abrir_caixa'))
        
        valor_fechamento = request.POST.get('valor_fechamento')
        print("Valor de fechamento:", valor_fechamento)
        
        try:
            print("Tentando fechar caixa")
            caixa.fechar_caixa(valor_fechamento)
            print("Caixa fechado com sucesso!")
            messages.add_message(request, constants.SUCCESS, "Caixa fechado com sucesso!")
            return redirect(reverse('caixa:relatorios'))
        except ValueError as e:
            print("Erro ao fechar caixa:", str(e))
            messages.add_message(request, constants.ERROR, str(e))
            return render(request, 'fechar_caixa.html', {'caixa': caixa})
    
    print("Request não é POST")
    return render(request, 'fechar_caixa.html')
# def fechar_caixa(request, caixa_id):
#     caixa = Caixa.objects.get(id=caixa_id)
#     if request.method == 'POST':
#         caixa = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
#         if not caixa:
#             messages.add_message(request, constants.ERROR, "Nenhum caixa aberto encontrado.")
#             return redirect(reverse('caixa:abrir_caixa'))

#         valor_fechamento = request.POST.get('valor_fechamento')
#         print(valor_fechamento)
#         try:
#             caixa.fechar_caixa(valor_fechamento)
#             messages.add_message(request, constants.SUCCESS, "Caixa fechado com sucesso!")
#             return redirect(reverse('caixa:relatorios'))
#         except ValueError as e:
#             messages.add_message(request, constants.ERROR, str(e))
#             return render(request, 'fechar_caixa.html', {'caixa': caixa})

#     return render(request, 'fechar_caixa.html')


@caixa_aberto_required
@login_required
def detalhe_caixa(request, caixa_id):
    caixa = Caixa.objects.get(id=caixa_id)
    sangrias = Sangria.objects.filter(caixa=caixa)
    return render(request, 'detalhe_caixa.html', {'caixa': caixa, 'sangrias': sangrias})


@caixa_aberto_required
@login_required
def receber_venda(request, venda_id):
    print("Iniciando função receber_venda")
    try:
        venda = Venda.objects.get(id=venda_id, status_pagamento='Fechada')
        print("Venda encontrada:", venda)
    except Venda.DoesNotExist:
        print("Venda não encontrada")
        messages.error(request, "Não há vendas a receber no momento.")
        return redirect(reverse('caixa:receber_vendas'))  # Redireciona para outra página ou retorna outra ação

    if request.method == 'POST':
        print("Requisição POST recebida")
        forma_pagamento = request.POST.get('forma_pagamento')
        print("Forma de pagamento:", forma_pagamento)
        venda.forma_pagamento = forma_pagamento
        
        # Implementar lógica de comissão do barbeiro aqui
        servico = venda.agendamento.servico
        print("Serviço:", servico)
        comissao = (servico.preco * servico.comissao_porcentagem) / 100
        print("Comissão:", comissao)
        barbeiro = venda.barbeiro
        print("Barbeiro:", barbeiro)
        barbeiro.saldo_comissao += comissao
        barbeiro.save()
        print("Barbeiro salvo com sucesso")
        
        venda.status_pagamento = 'Pago'
        venda.save()
        print("Venda salva com sucesso")

        # Atualizar status do agendamento para 'finalizado'
        agendamento = venda.agendamento
        agendamento.status = 'finalizado'
        agendamento.save()
        print("Status do agendamento atualizado para finalizado")

        
        # Atualizar valor total do caixa
        caixa = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
        print("Caixa:", caixa)
        if caixa:
            caixa.atualizar_valor_total(venda.id)
            print("Valor total do caixa atualizado com sucesso")
        else:
            print("Erro: Caixa não encontrado ou não está aberto")
        
        messages.success(request, "Venda recebida com sucesso!")
        return redirect(reverse('caixa:vendas_diarias'))

    cliente = f"{venda.agendamento.cliente.first_name} {venda.agendamento.cliente.last_name}"
    print("Cliente:", cliente)
    servico = venda.agendamento.servico.nome
    print("Serviço:", servico)
    servico_valor = venda.agendamento.servico.preco
    print("Valor do serviço:", servico_valor)
    barbeiro = f"{venda.barbeiro.user.first_name} {venda.barbeiro.user.last_name}"
    print("Barbeiro:", barbeiro)
    produtos_venda = VendaProduto.objects.filter(venda=venda)
    print("Produtos da venda:", produtos_venda)

    return render(request, 'receber_venda.html', {
        'venda': venda,
        'cliente': cliente,
        'servico': servico,
        'servico_valor': servico_valor,
        'barbeiro': barbeiro,
        'produtos_venda': produtos_venda,
    })


# def receber_venda(request, venda_id):
#     try:
#         venda = Venda.objects.get(id=venda_id, status_pagamento='Fechada')
#     except Venda.DoesNotExist:
#         messages.error(request, "Não há vendas a receber no momento.")
#         return redirect(reverse('caixa:receber_vendas'))  # Redireciona para outra página ou retorna outra ação

#     if request.method == 'POST':
#         forma_pagamento = request.POST.get('forma_pagamento')
#         venda.forma_pagamento = forma_pagamento
        
#         # Implementar lógica de comissão do barbeiro aqui
#         servico = venda.agendamento.servico
#         comissao = (servico.preco * servico.comissao_porcentagem) / 100
#         barbeiro = venda.barbeiro
#         barbeiro.saldo_comissao += comissao
#         barbeiro.save()
        
#         venda.status_pagamento = 'Pago'
#         venda.save()
        
#         # Atualizar valor total do caixa
#         caixa = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
#         if caixa:
#             caixa.atualizar_valor_total()
        
#         messages.success(request, "Venda recebida com sucesso!")
#         return redirect(reverse('caixa:vendas_diarias'))

#     cliente = f"{venda.agendamento.cliente.first_name} {venda.agendamento.cliente.last_name}"
#     servico = venda.agendamento.servico.nome
#     servico_valor = venda.agendamento.servico.preco
#     barbeiro = f"{venda.barbeiro.user.first_name} {venda.barbeiro.user.last_name}"
#     produtos_venda = VendaProduto.objects.filter(venda=venda)

#     return render(request, 'receber_venda.html', {
#         'venda': venda,
#         'cliente': cliente,
#         'servico': servico,
#         'servico_valor': servico_valor,
#         'barbeiro': barbeiro,
#         'produtos_venda': produtos_venda,
#     })

@login_required
@caixa_aberto_required
def aplicar_desconto(request):
    if request.method == 'POST':
        Desconto = request.POST.get('Desconto')
        # Implementar a lógica de aplicação de desconto aqui
        messages.add_message(request, constants.SUCCESS, "Desconto aplicado com sucesso!")
        return redirect(reverse('caixa:vendas_diarias'))
    return render(request, 'aplicar_desconto.html')



def sangria(request, caixa_id):
    caixa = Caixa.objects.filter(id=caixa_id, funcionario=request.user, aberto=True).first()
    if not caixa:
        messages.error(request, "Erro: Não há um caixa aberto.")
        return redirect(reverse('caixa:vendas_diarias'))

    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        valor = Decimal(request.POST.get('valor')).quantize(Decimal('0.01'))
        
        # Atualizar o valor total do caixa
        caixa.valor_total -= valor
        caixa.save()

        if valor > caixa.valor_total:
            messages.error(request, "Erro: Valor da sangria não pode ser maior que o valor total do caixa.")
            # Reverter a atualização do valor total do caixa
            caixa.valor_total += valor
            caixa.save()
        else:
            # Registrar a operação de sangria
            Sangria.objects.create(
                caixa=caixa,
                valor=valor,
                motivo=motivo
            )

            messages.success(request, "Sangria realizada com sucesso!")
            return redirect(reverse('caixa:vendas_diarias'))

    return render(request, 'sangria.html', {'caixa': caixa})

@login_required
@caixa_aberto_required
def vendas_diarias(request):
    vendas = Venda.objects.filter(status_pagamento='Pago')
    return render(request, 'vendas_diarias.html', {'vendas': vendas})

@login_required
def detalhes_venda_caixa(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    cliente = venda.agendamento.cliente.get_full_name()
    servico = venda.agendamento.servico.nome
    servico_valor = venda.agendamento.servico.preco
    barbeiro = venda.barbeiro
    usuario_recebedor = Caixa.objects.filter(funcionario=request.user, aberto=True).last()  # Obter o funcionário responsável pelo caixa
    data_recebimento = venda.data_hora_venda
    produtos_venda = venda.vendaproduto_set.all()
    

    return render(request, 'detalhes_venda_caixa.html', {
        'venda': venda,
        'cliente': cliente,
        'servico': servico,
        'barbeiro': barbeiro,
        'usuario_recebedor': usuario_recebedor,
        'data_recebimento': data_recebimento,
        'produtos_venda': produtos_venda,
        'servico_valor': servico_valor,
        
    })
# def caixa(request, pk):
#     venda = get_object_or_404(Venda, pk=pk)
#     qr_code_pix_base64 = None

#     if request.method == 'POST':
#         forma_pagamento = request.POST.get('forma_pagamento')
        
#         if forma_pagamento == 'Pix':
#             # Gera o QR Code Pix
#             chave_pix = venda.chave_pix
#             qr_code = QRCode(
#                 version=1,
#                 error_correction=constants.ERROR_CORRECT_Q,
#                 box_size=10,
#                 border=4,
#             )
#             qr_code.add_data(f"pix://{chave_pix}")
#             qr_code.make(fit=True)
#             img = qr_code.make_image(fill_color="black", back_color="white")
#             buffer = BytesIO()
#             img.save(buffer, format="PNG")
#             qr_code_pix_bytes = buffer.getvalue()
#             qr_code_pix_base64 = base64.b64encode(qr_code_pix_bytes).decode("utf-8")
        
#         venda.status_pagamento = 'Pago'
#         venda.forma_pagamento = forma_pagamento  # Adicione um campo `forma_pagamento` no modelo Venda
#         venda.save()
#         venda.barbeiro.saldo_comissao += venda.valor_comissao
#         venda.barbeiro.save()
#         return redirect(reverse('caixa:caixa', args=[pk]))

#     return render(request, 'caixa.html', {'venda': venda, 'qr_code_pix_base64': qr_code_pix_base64})

