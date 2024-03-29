# Generated by Django 3.0.12 on 2023-09-13 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extranet', '0004_speciesharvest'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Applied',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                        ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                        ('movement_type', models.CharField(max_length=7, verbose_name='Tipo Movimiento')),
                        ('voucher', models.CharField(max_length=16, verbose_name='Comprobante')),
                        ('voucher_date', models.DateField(null=True, verbose_name='Fecha Comprobante')),
                        ('expiration_date', models.DateField(null=True, verbose_name='Fecha Vencimiento')),
                        ('issue_date', models.DateField(null=True, verbose_name='Fecha Emision')),
                        ('concept', models.CharField(max_length=200, verbose_name='Concepto')),
                        ('cta_cte', models.CharField(max_length=1, verbose_name='Codigo de Cta. Cte.')),
                        ('cta_cte_description', models.CharField(max_length=50, verbose_name='Descripcion de Cta. Cte.')),
                        ('currency', models.CharField(max_length=1, verbose_name='Moneda')),
                        ('amount_sign', models.FloatField(verbose_name='Importe Signo')),
                        ('exchange_rate', models.FloatField(verbose_name='Tipo de Cambio Emisión')),
                    ],
                    options={
                        'verbose_name': 'Cuenta Corriente Aplicada',
                        'verbose_name_plural': 'Cuentas Corrientes Aplicadas',
                    },
                ),
            ],
            # Table already exists. See website/migrations/0013_delete_applied.py
            database_operations=[],
        ),
    ]
