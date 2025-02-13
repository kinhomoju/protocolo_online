from django.db import models, transaction
from django.utils import timezone
from django.conf import settings

class Protocolo(models.Model):
    numero = models.CharField(max_length=30, unique=True, editable=False)
    descricao = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('pago', 'Pago'),
        ('analise', 'Em Análise'),
        ('rejeitado', 'Rejeitado'),
        # ('devolvido', 'Devolvido'),
        ('pendente', 'Pendente'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='protocolos'
    )

    def save(self, *args, **kwargs):
        if not self.numero:
            now = timezone.localtime(timezone.now())
            # Gera o prefixo com a data (DDMMAAAA)
            date_prefix = now.strftime('%d%m%Y')
            # Gera a parte de hora (HHMMSS)
            time_part = now.strftime('%H%M%S')
            # Em vez de salvar imediatamente para gerar a sequência, vamos calcular quantos protocolos já foram criados hoje.
            # Como a numeração reinicia diariamente, filtramos pelo prefixo de data.
            with transaction.atomic():
                count = Protocolo.objects.filter(numero__startswith=date_prefix).count() + 1
                sequence = str(count).zfill(4)
                self.numero = date_prefix + time_part + sequence
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero
