# Generated by Django 3.0.12 on 2023-09-13 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extranet', '0005_applied'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='CtaCte',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                        ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                        ('initial_balance_countable', models.FloatField(verbose_name='Saldo Inicial Contable')),
                        ('balance', models.FloatField(verbose_name='Saldo')),
                        ('voucher', models.CharField(max_length=16, verbose_name='Comprobante')),
                        ('voucher_date', models.DateField(null=True, verbose_name='Fecha Comprobante')),
                        ('concept', models.CharField(max_length=200, verbose_name='Concepto')),
                        ('currency', models.CharField(max_length=1, verbose_name='Moneda')),
                        ('movement_type', models.CharField(max_length=7, verbose_name='Tipo Movimiento')),
                        ('exchange_rate', models.FloatField(verbose_name='Tipo de Cambio Emisión')),
                        ('date_1', models.DateField(null=True, verbose_name='Fecha Vencimiento')),
                        ('date_2', models.DateField(null=True, verbose_name='Fecha Emisión')),
                        ('amount_sign', models.FloatField(verbose_name='Importe Signo')),
                        ('cta_cte', models.CharField(max_length=80, verbose_name='Tipo Cta. Cte.')),
                        ('cta_cte_name', models.CharField(max_length=80, verbose_name='Descripcion Cta. Cte.')),
                    ],
                    options={
                        'verbose_name': 'Cuenta Corriente',
                        'verbose_name_plural': 'Cuentas Corrientes',
                    },
                ),
            ],
            # Table already exists. See website/migrations/0014_delete_ctacte.py
            database_operations=[],
        ),
    ]