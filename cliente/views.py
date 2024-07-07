from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from agendamentos.models import Agendamento
import logging

# cliente/views.py


logger = logging.getLogger(__name__)

@login_required
def home(request):
    logger.debug(f"User: {request.user}")
    agendamentos = Agendamento.objects.filter(cliente=request.user)
    return render(request, 'home.html', {'agendamentos': agendamentos})
