from .models import Caixa

def caixa_aberto(request):
    if request.user.is_authenticated:
        try:
            caixa_aberto = Caixa.objects.filter(funcionario=request.user, aberto=True).last()
        except Caixa.DoesNotExist:
            caixa_aberto = None
    else:
        caixa_aberto = None

    return {
        'caixa_aberto': caixa_aberto
    }