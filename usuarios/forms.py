from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Perfil  # Supondo que você tenha um modelo Perfil para dados complementares

class UsuarioCadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'username', 'email', 'password1', 'password2']

class UsuarioLoginForm(AuthenticationForm):
    pass

# Formulário para dados complementares de Pessoa Jurídica (PJ)
class PerfilPJForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['cnpj', 'nome_empresa', 'nome_fantasia', 'atividade_principal',
                  'endereco', 'numero', 'complemento', 'cep', 'bairro', 'cidade', 'estado']
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'atividade_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulário para dados complementares de Pessoa Física (PF)
class PerfilPFForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['secretaria', 'setor', 'cargo']
        widgets = {
            'secretaria': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }
