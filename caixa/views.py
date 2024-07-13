from django.shortcuts import render, get_object_or_404, redirect
from vendas.models import Venda
from django.http import JsonResponse
from qrcode import QRCode, constants
# from qrcode import QRCode, ErrorCorrectLevel, QRCodeVersion
from io import BytesIO
import base64
from .models import Caixa
from vendas.models import Venda
from django.urls import reverse_lazy, reverse

def caixa_vendas(request):
    vendas = Venda.objects.filter(status_pagamento='Fechado')
    return render(request, 'caixa_vendas.html', {'vendas': vendas})

def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'detalhe_venda.html', {'venda': venda})

def caixa(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    qr_code_pix_base64 = None

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        
        if forma_pagamento == 'Pix':
            # Gera o QR Code Pix
            chave_pix = venda.chave_pix
            qr_code = QRCode(
                version=1,
                error_correction=constants.ERROR_CORRECT_Q,
                box_size=10,
                border=4,
            )
            qr_code.add_data(f"pix://{chave_pix}")
            qr_code.make(fit=True)
            img = qr_code.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_pix_bytes = buffer.getvalue()
            qr_code_pix_base64 = base64.b64encode(qr_code_pix_bytes).decode("utf-8")
        
        venda.status_pagamento = 'Pago'
        venda.forma_pagamento = forma_pagamento  # Adicione um campo `forma_pagamento` no modelo Venda
        venda.save()
        venda.barbeiro.saldo_comissao += venda.valor_comissao
        venda.barbeiro.save()
        return redirect(reverse('caixa:caixa', args=[pk]))

    return render(request, 'caixa.html', {'venda': venda, 'qr_code_pix_base64': qr_code_pix_base64})

def gerar_qr_code_pix(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    chave_pix = venda.chave_pix

    qr_code = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qr_code.add_data(f"pix://{chave_pix}")
    qr_code.make(fit=True)

    img = qr_code.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_pix_bytes = buffer.getvalue()
    qr_code_pix_base64 = base64.b64encode(qr_code_pix_bytes).decode("utf-8")

    return JsonResponse({'qr_code_pix': qr_code_pix_base64})

#@login_required
def abrir_caixa(request):
    if request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == request.user.caixa.senha:  # Verifica se a senha é válida
            caixa = Caixa.objects.create(usuario=request.user)
            return redirect('caixa_aberto')
        else:
            return render(request, 'abrir_caixa.html', {'erro': 'Senha inválida'})
    return render(request, 'abrir_caixa.html')



def fechar_vendas(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    venda.status_pagamento = 'Fechado'
    venda.save()
    return redirect(reverse_lazy('caixa:vendas_aberta_caixa'))

def vendas_aberta_caixa(request):
    vendas_abertas = Venda.objects.filter()
    return render(request, 'vendas_aberta_caixa.html', {'vendas_abertas': vendas_abertas})
