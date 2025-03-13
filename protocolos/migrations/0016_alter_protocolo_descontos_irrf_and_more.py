# Generated by Django 5.1.6 on 2025-03-13 01:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "protocolos",
            "0015_alter_protocolo_cnpj_alter_protocolo_nome_empresa_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocolo",
            name="descontos_irrf",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name="protocolo",
            name="descontos_iss",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AlterField(
            model_name="protocolo",
            name="valor_bruto",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=14
            ),
        ),
        migrations.AlterField(
            model_name="protocolo",
            name="valor_liquido",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.CreateModel(
            name="ProtocoloAnexo",
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
                ("arquivo", models.FileField(upload_to="anexos/")),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                (
                    "protocolo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="anexos",
                        to="protocolos.protocolo",
                    ),
                ),
            ],
        ),
    ]
