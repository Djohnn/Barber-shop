# from django import forms
# from.models import Agendamento, Barbeiro, Produto
# from estoque.models import Produto

# class VendaForm(forms.Form):
#     agendamento = forms.ModelChoiceField(queryset=Agendamento.objects.filter(status='pendente'), label='Selecione um agendamento')
#     barbeiro = forms.ModelChoiceField(queryset=Barbeiro.objects.all(), label='Selecione um barbeiro')
#     produtos = forms.CharField(label='Digite o nome do produto', widget=forms.TextInput(attrs={'placeholder': 'Digite o nome do produto'}))
#     desconto = forms.DecimalField(label='Desconto', initial=0.00, max_digits=5, decimal_places=2)
#     forma_pagamento = forms.ChoiceField(label='Forma de Pagamento', choices=[('dinheiro', 'Dinheiro')])


from django import forms
from .models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['agendamento', 'barbeiro', 'desconto', 'forma_pagamento']
