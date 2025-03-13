from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
import os

class Protocolo(models.Model):
    TIPO_PF_CHOICES = [
        ('RECIBO', 'Recibo'),
        ('NOTA_FISCAL', 'Nota Fiscal'),
    ]

    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('analise', 'Em Análise'),
        ('rejeitado', 'Rejeitado'),
        ('pendente', 'Pendente'),
    ]

    TIPO_NF_CHOICES = [
        ('NFe', 'Nota Fiscal (NFe)'),
        ('NFSe', 'Nota Fiscal de Serviços (NFSe)'),
    ]

    numero = models.CharField(max_length=20, unique=True, editable=False)
    tipo_pf = models.CharField(max_length=20, choices=TIPO_PF_CHOICES, blank=True)
    tipo_nf = models.CharField(max_length=20, choices=TIPO_NF_CHOICES, blank=True)
    descontar_iss = models.BooleanField(default=False)
    simples_nacional = models.BooleanField(default=False)
    numero_recibo = models.CharField(max_length=20, unique=True, editable=False)
    numero_nota_fiscal = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255, default='Endereço padrão')
    descricao_servicos = models.TextField(max_length=150)
    valor_bruto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    descontos_iss = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descontos_irrf = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    data = models.DateField(default=timezone.now)
    cnpj = models.CharField(max_length=18, blank=True)
    nome_empresa = models.CharField(max_length=255, blank=True)
    data_nota_fiscal = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='protocolos')
    data_hora_lancamento = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero:
            now = timezone.localtime(timezone.now())
            date_prefix = now.strftime('%d%m%Y')
            time_part = now.strftime('%H%M%S')
            with transaction.atomic():
                count = Protocolo.objects.filter(numero__startswith=date_prefix).count() + 1
                sequence = str(count).zfill(4)
                self.numero = date_prefix + time_part + sequence
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero

def protocolo_anexo_upload_to(instance, filename):
    return os.path.join('anexos', f'protocolo_{instance.protocolo.numero}', filename)

class ProtocoloAnexo(models.Model):
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to=protocolo_anexo_upload_to)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo {self.id} do Protocolo {self.protocolo.numero}"
