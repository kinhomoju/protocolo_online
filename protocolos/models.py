from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
import os

# Modelo Base para Protocolo (PF e PJ herdam dele)
class Protocolo(models.Model):
    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('analise', 'Em Análise'),
        ('rejeitado', 'Rejeitado'),
        ('pendente', 'Pendente'),
    ]

    numero = models.CharField(max_length=20, unique=True, editable=False)
    data_hora_lancamento = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(max_length=150, blank=True)
    valor_bruto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descontos_iss = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descontos_irrf = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True  # Este modelo não será salvo diretamente no banco

    def save(self, *args, **kwargs):
        if not self.numero:
            now = timezone.localtime(timezone.now())
            date_prefix = now.strftime('%d%m%Y')
            time_part = now.strftime('%H%M%S')
            with transaction.atomic():
                # Contabiliza PF e PJ juntos para garantir unicidade
                count = (ProtocoloPF.objects.filter(numero__startswith=date_prefix).count() +
                         ProtocoloPJ.objects.filter(numero__startswith=date_prefix).count() + 1)
                sequence = str(count).zfill(4)
                self.numero = date_prefix + time_part + sequence
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero


# Modelo para Protocolo PF (herda de Protocolo)
class ProtocoloPF(Protocolo):
    TIPO_PF_CHOICES = [
        ('RECIBO', 'Recibo'),
        ('NOTA_FISCAL', 'Nota Fiscal'),
    ]

    TIPO_NF_CHOICES = [
        ('NFe', 'Nota Fiscal (NFe)'),
        ('NFSe', 'Nota Fiscal de Serviços (NFSe)'),
        ('NFAe', 'Nota Fiscal Avulsa Eletrônica'),
    ]

    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    tipo_pf = models.CharField(max_length=20, choices=TIPO_PF_CHOICES)
    tipo_nf = models.CharField(max_length=20, choices=TIPO_NF_CHOICES)
    numero_nota_fiscal = models.CharField(max_length=20)
    data_da_nota_fiscal = models.DateField()


# Modelo para Protocolo PJ (herda de Protocolo)
class ProtocoloPJ(Protocolo):
    TIPO_NF_CHOICES = [
        ('NFe', 'Nota Fiscal (NFe)'),
        ('NFSe', 'Nota Fiscal de Serviços (NFSe)'),
    ]

    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, blank=True)
    endereco = models.CharField(max_length=255, default='Endereço padrão')
    tipo_nf = models.CharField(max_length=20, choices=TIPO_NF_CHOICES, blank=True)
    simples_nacional = models.BooleanField(default=False)
    descontar_iss = models.BooleanField(default=False)
    numero_nota_fiscal = models.CharField(max_length=20, blank=True)
    data_nota_fiscal = models.DateField(null=True, blank=True)


# Função para gerar caminho do anexo (agora suporta PF e PJ)
def protocolo_anexo_upload_to(instance, filename):
    return os.path.join('anexos', f'protocolo_{instance.protocolo.numero}', filename)


# Modelo para anexos (aceita PF e PJ)
class ProtocoloAnexo(models.Model):
    protocolo_pf = models.ForeignKey(ProtocoloPF, null=True, blank=True, on_delete=models.CASCADE, related_name='anexos_pf')
    protocolo_pj = models.ForeignKey(ProtocoloPJ, null=True, blank=True, on_delete=models.CASCADE, related_name='anexos_pj')
    arquivo = models.FileField(upload_to=protocolo_anexo_upload_to)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo {self.id} do Protocolo {self.get_protocolo_numero()}"

    def get_protocolo_numero(self):
        return self.protocolo_pf.numero if self.protocolo_pf else self.protocolo_pj.numero
