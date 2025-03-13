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
            'descricao_servicos': forms.Textarea(attrs={'class': 'form-control'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
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
        fields = ['descricao_servicos', 'valor_bruto', 'descontos_iss', 'descontos_irrf', 'valor_liquido', 'tipo_nf', 'descontar_iss', 'simples_nacional', 'numero_nota_fiscal']

class ProtocoloAnexoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloAnexo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
