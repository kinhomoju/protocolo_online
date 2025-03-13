from django import forms
from .models import Protocolo, ProtocoloAnexo

from django import forms
from .models import Protocolo, ProtocoloAnexo

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
            'descricao_servicos': forms.Textarea(attrs={'class': 'form-control'}),  # Removido maxlength
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
    tipo_nf = forms.ChoiceField(
        choices=Protocolo.TIPO_NF_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Nota Fiscal'
    )
    descontar_iss = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Descontar ISS'
    )
    simples_nacional = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Simples Nacional'
    )
    numero_nota_fiscal = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nº da NF...'}),
        label='nº da NF'
    )

    class Meta:
        model = Protocolo
        fields = ['tipo_nf', 'descontar_iss', 'simples_nacional', 'numero_nota_fiscal', 'valor_bruto', 'descontos_iss', 'descontos_irrf', 'valor_liquido', 'descricao_servicos', 'cnpj', 'nome_empresa', 'endereco', 'data_nota_fiscal', 'status']
        widgets = {
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor bruto...'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite os descontos do ISS...'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite os descontos do IRRF...'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor líquido...'}),
            'descricao_servicos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva os serviços prestados...'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CNPJ...'}),
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'tipo_nf': 'Tipo de Nota Fiscal',
            'descontar_iss': 'Descontar ISS',
            'simples_nacional': 'Simples Nacional',
            'numero_nota_fiscal': 'nº da NF',
            'valor_bruto': 'Valor Bruto',
            'descontos_iss': 'Valor ISS',
            'descontos_irrf': 'Valor IRRF',
            'valor_liquido': 'Valor Líquido',
            'descricao_servicos': 'Descrição dos Serviços',
            'cnpj': 'CNPJ',
            'nome_empresa': 'Nome da Empresa',
            'endereco': 'Endereço',
            'data_nota_fiscal': 'Data da NF',
            'status': 'Status',
        }

class ProtocoloAnexoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloAnexo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),  # Removido multiple: True
        }
