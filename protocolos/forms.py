from django import forms
from .models import ProtocoloPF, ProtocoloPJ, ProtocoloAnexo

class ProtocoloPFForm(forms.ModelForm):
    class Meta:
        model = ProtocoloPF
        fields = '__all__'
        widgets = {
            'tipo_pf': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_hora_lancamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProtocoloPJForm(forms.ModelForm):
    class Meta:
        model = ProtocoloPJ
        fields = [
            'tipo_nf', 'simples_nacional', 'descontar_iss', 'numero_nota_fiscal', 
            'data_nota_fiscal', 'descricao', 'valor_bruto', 'descontos_iss', 
            'descontos_irrf', 'valor_liquido', 'nome', 'endereco'
        ]
        widgets = {
            'tipo_nf': forms.Select(attrs={'class': 'form-control'}),
            'simples_nacional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descontar_iss': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_nota_fiscal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'digite o nº da NF...'}),
            'data_nota_fiscal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva os serviços prestados...'}),
            'valor_bruto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'digite o valor bruto...'}),
            'descontos_iss': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'digite o ISS...'}),
            'descontos_irrf': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'digite o IRRF...'}),
            'valor_liquido': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_nf = cleaned_data.get('tipo_nf')
        simples_nacional = cleaned_data.get('simples_nacional')
        descontar_iss = cleaned_data.get('descontar_iss')
        descontos_irrf = cleaned_data.get('descontos_irrf')

        if tipo_nf == 'NFSe' and not simples_nacional and not descontar_iss and not descontos_irrf:
            self.add_error('descontos_irrf', 'Este campo é obrigatório quando "Simples Nacional" e "Descontar ISS" não estão selecionados.')

        return cleaned_data

class ProtocoloAnexoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloAnexo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
