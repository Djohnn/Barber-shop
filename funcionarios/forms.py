from django import forms
from usuarios.models import Users

class FuncionarioForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'endereco', 'cargo']
        widgets = {
            'cargo': forms.Select(choices=[
                ('V', 'Vendedor'),
                ('G', 'Gerente'),
                ('C', 'Caixa'),
                ('B', 'Barbeiro')
            ])
        }
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            raise forms.ValidationError('Senhas não conferem')
        return cleaned_data

class CriarSenhaForm(forms.Form):
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    def clean(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            raise forms.ValidationError('Senhas não conferem')
        return self.cleaned_data