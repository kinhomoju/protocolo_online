# Generated by Django 5.1.6 on 2025-03-06 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("protocolos", "0005_protocolo_numero_nota_fiscal"),
    ]

    operations = [
        migrations.AddField(
            model_name="protocolo",
            name="numero_recibo",
            field=models.CharField(
                default="0e96611939374156a294da0932f58970",
                editable=False,
                max_length=20,
            ),
        ),
    ]
