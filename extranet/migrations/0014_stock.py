# Generated by Django 4.2.5 on 2023-10-31 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extranet', '0013_applied_affected_balance_applied_affected_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(db_index=True, verbose_name='Cuenta Algoritmo')),
                ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('speciesharvest', models.CharField(max_length=8, null=True, verbose_name='Especie Cosecha')),
                ('deliveries', models.IntegerField(verbose_name='Entregas')),
                ('certificated', models.IntegerField(verbose_name='Certificado')),
                ('uncertified', models.IntegerField(verbose_name='Sin Certificar')),
                ('withdrawals', models.IntegerField(verbose_name='Retiros')),
                ('sales', models.IntegerField(verbose_name='Ventas')),
                ('settled', models.IntegerField(verbose_name='Liquidado')),
                ('not_settled', models.IntegerField(verbose_name='Sin Liquidar')),
                ('to_set', models.IntegerField(verbose_name='A Fijar')),
                ('balance', models.IntegerField(verbose_name='Saldo Neto')),
                ('trade_balance', models.FloatField(verbose_name='Saldo Comercial')),
            ],
            options={
                'verbose_name': 'Stock por Productor',
                'verbose_name_plural': 'Stock por Productor',
            },
        ),
    ]
