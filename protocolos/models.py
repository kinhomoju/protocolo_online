from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
import uuid

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

    numero = models.CharField(max_length=20, unique=True, editable=False)  # Descomente este campo
    tipo_pf = models.CharField(max_length=20, choices=TIPO_PF_CHOICES, null=True, blank=True)
    numero_recibo = models.CharField(max_length=20, unique=True, editable=False, default=uuid.uuid4().hex)
    numero_nota_fiscal = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    nome = models.CharField(max_length=255, default='Nome padrão')
    endereco = models.CharField(max_length=255, default='Endereço padrão')
    descricao_servicos = models.TextField(default='Descrição padrão')
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descontos_iss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descontos_irrf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data = models.DateField(default=timezone.now)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    nome_empresa = models.CharField(max_length=255, null=True, blank=True)
    data_nota_fiscal = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='protocolos')
    data_hora_lancamento = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
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
