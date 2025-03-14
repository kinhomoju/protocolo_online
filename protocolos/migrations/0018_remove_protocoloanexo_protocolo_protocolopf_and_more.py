# Generated by Django 5.1.6 on 2025-03-14 03:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("protocolos", "0017_alter_protocoloanexo_arquivo"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="protocoloanexo",
            name="protocolo",
        ),
        migrations.CreateModel(
            name="ProtocoloPF",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numero",
                    models.CharField(editable=False, max_length=20, unique=True),
                ),
                (
                    "data_hora_lancamento",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("descricao", models.TextField(blank=True, max_length=150)),
                (
                    "valor_bruto",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "descontos_iss",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "descontos_irrf",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "valor_liquido",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pago", "Pago"),
                            ("analise", "Em Análise"),
                            ("rejeitado", "Rejeitado"),
                            ("pendente", "Pendente"),
                        ],
                        default="pendente",
                        max_length=20,
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("cpf", models.CharField(max_length=14)),
                ("rg", models.CharField(max_length=20)),
                ("endereco", models.CharField(max_length=255)),
                (
                    "tipo_pf",
                    models.CharField(
                        choices=[("RECIBO", "Recibo"), ("NOTA_FISCAL", "Nota Fiscal")],
                        max_length=20,
                    ),
                ),
                (
                    "tipo_nf",
                    models.CharField(
                        choices=[
                            ("NFe", "Nota Fiscal (NFe)"),
                            ("NFSe", "Nota Fiscal de Serviços (NFSe)"),
                            ("NFAe", "Nota Fiscal Avulsa Eletrônica"),
                        ],
                        max_length=20,
                    ),
                ),
                ("numero_nota_fiscal", models.CharField(max_length=20)),
                ("data_da_nota_fiscal", models.DateField()),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="protocoloanexo",
            name="protocolo_pf",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="anexos_pf",
                to="protocolos.protocolopf",
            ),
        ),
        migrations.CreateModel(
            name="ProtocoloPJ",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "numero",
                    models.CharField(editable=False, max_length=20, unique=True),
                ),
                (
                    "data_hora_lancamento",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("descricao", models.TextField(blank=True, max_length=150)),
                (
                    "valor_bruto",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "descontos_iss",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "descontos_irrf",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "valor_liquido",
                    models.DecimalField(decimal_places=2, default=0, max_digits=14),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pago", "Pago"),
                            ("analise", "Em Análise"),
                            ("rejeitado", "Rejeitado"),
                            ("pendente", "Pendente"),
                        ],
                        default="pendente",
                        max_length=20,
                    ),
                ),
                ("nome", models.CharField(max_length=150)),
                ("cnpj", models.CharField(blank=True, max_length=18)),
                (
                    "endereco",
                    models.CharField(default="Endereço padrão", max_length=255),
                ),
                (
                    "tipo_nf",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NFe", "Nota Fiscal (NFe)"),
                            ("NFSe", "Nota Fiscal de Serviços (NFSe)"),
                        ],
                        max_length=20,
                    ),
                ),
                ("simples_nacional", models.BooleanField(default=False)),
                ("descontar_iss", models.BooleanField(default=False)),
                ("numero_nota_fiscal", models.CharField(blank=True, max_length=20)),
                ("data_nota_fiscal", models.DateField(blank=True, null=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="protocoloanexo",
            name="protocolo_pj",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="anexos_pj",
                to="protocolos.protocolopj",
            ),
        ),
        migrations.DeleteModel(
            name="Protocolo",
        ),
    ]
