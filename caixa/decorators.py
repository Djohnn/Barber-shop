from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Caixa

def caixa_aberto_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            caixa_aberto = Caixa.objects.filter(funcionario=request.user, aberto=True).exists()
            if not caixa_aberto:
                messages.add_message(request, constants.ERROR, "O caixa não está aberto.")
                return redirect(reverse('caixa:abrir_caixa'))
        except Caixa.DoesNotExist:
            messages.add_message(request, constants.ERROR, "O caixa não está aberto.")
            return redirect(reverse('caixa:abrir_caixa'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
