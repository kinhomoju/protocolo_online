from django import forms
from .models import Protocolo

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = ['descricao', 'status']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição do protocolo'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProtocoloPFForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = ['tipo_pf', 'cpf', 'nome', 'endereco', 'descricao_servicos', 'valor_bruto', 'descontos_iss', 'descontos_irrf', 'valor_liquido', 'data', 'data_nota_fiscal', 'status']
        widgets = {
            'tipo_pf': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_servicos': forms.Textarea(attrs={'class': 'form-control'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'tipo_pf': 'Tipo PF',
            'cpf': 'CPF',
            'nome': 'Nome',
            'endereco': 'Endereço',
            'descricao_servicos': 'Descrição dos Serviços',
            'valor_bruto': 'Valor Bruto',
            'descontos_iss': 'Valor ISS',
            'descontos_irrf': 'Valor IRRF',
            'valor_liquido': 'Valor Líquido',
            'data': 'Data',
            'data_nota_fiscal': 'Data da NF',
            'status': 'Status',
        }

class ProtocoloPJForm(forms.ModelForm):
    numero_nota_fiscal = forms.CharField(
        max_length=20, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'digite o nº da NF...'}),
        label='nº da NF'
    )

    class Meta:
        model = Protocolo
        fields = ['cnpj', 'nome_empresa', 'endereco', 'descricao_servicos', 'valor_bruto', 'descontos_iss', 'descontos_irrf', 'valor_liquido', 'data_nota_fiscal', 'numero_nota_fiscal', 'status']
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'digite o CNPJ...'}),
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_servicos': forms.Textarea(attrs={'class': 'form-control'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero_nota_fiscal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'digite o nº da NF...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cnpj': 'CNPJ',
            'nome_empresa': 'Nome da Empresa',
            'endereco': 'Endereço',
            'descricao_servicos': 'Descrição dos Serviços',
            'valor_bruto': 'Valor Bruto',
            'descontos_iss': 'Valor ISS',
            'descontos_irrf': 'Valor IRRF',
            'valor_liquido': 'Valor Líquido',
            'data_nota_fiscal': 'Data da NF',
            'numero_nota_fiscal': 'nº da NF',
            'status': 'Status',
        }
