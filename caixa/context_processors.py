from .models import Caixa

def caixa_aberto(request):
    caixa_aberto = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
    return {
        'caixa_aberto': caixa_aberto
    }
