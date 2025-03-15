from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)  # Nome completo
    tipo = models.CharField(
        max_length=2,
        choices=[('PJ', 'Pessoa Jurídica'), ('SP', 'Servidor Público')],
        null=True,
        blank=True
    )
    is_master = models.BooleanField(default=False, verbose_name="É Master?")
    is_approved = models.BooleanField(default=False, verbose_name="Aprovado?")

    def save(self, *args, **kwargs):
        # Garantir que superusuários sejam aprovados automaticamente
        if self.is_superuser:
            self.is_approved = True
            self.is_master = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({'Master' if self.is_master else 'Usuário Comum'})"


class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')

    # **Pessoa Jurídica (PJ)**
    cnpj = models.CharField(max_length=20, blank=True, null=True, unique=True)
    nome_empresa = models.CharField(max_length=200, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    atividade_principal = models.CharField(max_length=200, blank=True, null=True)

    # **Servidor Público (SP)**
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)  # Adicionado CPF
    secretaria = models.CharField(max_length=200, blank=True, null=True)
    setor = models.CharField(max_length=200, blank=True, null=True)
    cargo = models.CharField(max_length=200, blank=True, null=True)

    # **Endereço**
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=5, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
