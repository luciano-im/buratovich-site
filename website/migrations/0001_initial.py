# Generated by Django 3.0.8 on 2020-07-26 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('wheat_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo')),
                ('wheat_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo')),
                ('wheat_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo')),
                ('wheat_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo')),
                ('wheat12_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo Art. 12')),
                ('wheat12_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo Art. 12')),
                ('wheat12_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo Art. 12')),
                ('wheat12_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Trigo Art. 12')),
                ('corn_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Maiz')),
                ('corn_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Maiz')),
                ('corn_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Maiz')),
                ('corn_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Maiz')),
                ('sunflower_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Girasol')),
                ('sunflower_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Girasol')),
                ('sunflower_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Girasol')),
                ('sunflower_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Girasol')),
                ('soy_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Soja')),
                ('soy_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Soja')),
                ('soy_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Soja')),
                ('soy_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Soja')),
                ('sorghum_ros', models.FloatField(blank=True, default=None, null=True, verbose_name='Sorgo')),
                ('sorghum_bas', models.FloatField(blank=True, default=None, null=True, verbose_name='Sorgo')),
                ('sorghum_qq', models.FloatField(blank=True, default=None, null=True, verbose_name='Sorgo')),
                ('sorghum_bb', models.FloatField(blank=True, default=None, null=True, verbose_name='Sorgo')),
            ],
            options={
                'verbose_name': 'Pizarra',
                'verbose_name_plural': 'Pizarras',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=80, verbose_name='Ciudad')),
                ('state', models.CharField(choices=[('BUE', 'Buenos Aires'), ('CHA', 'Chaco')], default='BUE', max_length=3, verbose_name='Provincia')),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
            },
        ),
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
                ('cta_cte', models.CharField(max_length=1, verbose_name='Tipo Cta. Cte.')),
                ('cta_cte_name', models.CharField(max_length=80, verbose_name='Descripcion Cta. Cte.')),
            ],
            options={
                'verbose_name': 'Cuenta Corriente',
                'verbose_name_plural': 'Cuentas Corrientes',
            },
        ),
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('dn_buy', models.FloatField(verbose_name='Dolar Nación')),
                ('dl_buy', models.FloatField(blank=True, default=None, null=True, verbose_name='Dolar Libre')),
                ('dn_sell', models.FloatField(verbose_name='Dolar Nación')),
                ('dl_sell', models.FloatField(blank=True, default=None, null=True, verbose_name='Dolar Libre')),
            ],
            options={
                'verbose_name': 'Moneda',
                'verbose_name_plural': 'Monedas',
            },
        ),
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                ('indicator', models.CharField(max_length=1, verbose_name='Indicador')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('speciesharvest', models.CharField(max_length=8, null=True, verbose_name='Especie Cosecha')),
                ('species_description', models.CharField(max_length=50, verbose_name='Especie y Cosecha')),
                ('field', models.IntegerField(verbose_name='Codigo de Campo')),
                ('field_description', models.CharField(max_length=100, verbose_name='Nombre de Campo')),
                ('date', models.DateField(null=True, verbose_name='Fecha')),
                ('voucher', models.CharField(max_length=16, verbose_name='Comprobante')),
                ('gross_kg', models.IntegerField(verbose_name='Peso Bruto')),
                ('humidity_percentage', models.FloatField(verbose_name='Humedad (%)')),
                ('humidity_reduction', models.FloatField(verbose_name='Merma de Humedad')),
                ('humidity_kg', models.IntegerField(verbose_name='Kilos de Humedad')),
                ('shaking_reduction', models.FloatField(verbose_name='Merma de Zarandeo')),
                ('shaking_kg', models.IntegerField(verbose_name='Kilos de Zarandeo')),
                ('volatile_reduction', models.FloatField(verbose_name='Merma Volatil')),
                ('volatile_kg', models.IntegerField(verbose_name='Kilos Volatil')),
                ('price_per_yard', models.FloatField(verbose_name='Precio por Quintal')),
                ('driver_code', models.IntegerField(verbose_name='Chofer')),
                ('driver_name', models.CharField(max_length=150, verbose_name='Nombre del Chofer')),
                ('factor', models.FloatField(verbose_name='Factor')),
                ('grade', models.IntegerField(verbose_name='Grado')),
                ('gluten', models.IntegerField(verbose_name='Gluten')),
                ('number_1116A', models.IntegerField(verbose_name='Numero 1116A')),
                ('km', models.IntegerField(verbose_name='Kilometros')),
                ('external_voucher_number', models.IntegerField(verbose_name='Numero Comprobante Externo')),
                ('service_billing_number', models.IntegerField(verbose_name='Numero Factura de Servicios')),
                ('service_billing_date', models.DateField(null=True, verbose_name='Fecha Factura de Servicios')),
                ('service_billing', models.CharField(max_length=50, verbose_name='Factura de Servicios')),
                ('to_date', models.DateField(null=True, verbose_name='Fecha Entrega Hasta')),
                ('observations', models.CharField(max_length=300, verbose_name='Observaciones')),
                ('follow_destination', models.CharField(max_length=2, verbose_name='Sigue a Destino')),
                ('net_weight', models.IntegerField(verbose_name='Peso Neto')),
                ('tare', models.IntegerField(verbose_name='Tara')),
            ],
            options={
                'verbose_name': 'Entregas',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('title', models.CharField(max_length=200, verbose_name='Titulo')),
                ('notification', models.TextField(verbose_name='Notificación')),
                ('active', models.BooleanField(default=True, verbose_name='Activa/Inactiva')),
                ('date_from', models.DateField(verbose_name='Vigencia Desde')),
                ('date_to', models.DateField(verbose_name='Vigencia Hasta')),
            ],
            options={
                'verbose_name': 'Notificación',
                'verbose_name_plural': 'Notificaciones',
            },
        ),
        migrations.CreateModel(
            name='Rain',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False, verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Lluvia',
                'verbose_name_plural': 'Lluvias',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('name', models.CharField(max_length=150, verbose_name='Razón Social')),
                ('indicator', models.CharField(max_length=1, verbose_name='Indicador')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('speciesharvest', models.CharField(max_length=8, null=True, verbose_name='Especie Cosecha')),
                ('species_description', models.CharField(max_length=50, verbose_name='Especie y Cosecha')),
                ('field', models.IntegerField(verbose_name='Codigo de Campo')),
                ('field_description', models.CharField(max_length=100, verbose_name='Nombre de Campo')),
                ('date', models.DateField(null=True, verbose_name='Fecha')),
                ('voucher', models.CharField(max_length=16, verbose_name='Comprobante')),
                ('gross_kg', models.IntegerField(verbose_name='Peso Bruto')),
                ('humidity_percentage', models.FloatField(verbose_name='Humedad (%)')),
                ('humidity_reduction', models.FloatField(verbose_name='Merma de Humedad')),
                ('humidity_kg', models.IntegerField(verbose_name='Kilos de Humedad')),
                ('shaking_reduction', models.FloatField(verbose_name='Merma de Zarandeo')),
                ('shaking_kg', models.IntegerField(verbose_name='Kilos de Zarandeo')),
                ('volatile_reduction', models.FloatField(verbose_name='Merma Volatil')),
                ('volatile_kg', models.IntegerField(verbose_name='Kilos Volatil')),
                ('price_per_yard', models.FloatField(verbose_name='Precio por Quintal')),
                ('driver_code', models.IntegerField(verbose_name='Chofer')),
                ('driver_name', models.CharField(max_length=150, verbose_name='Nombre del Chofer')),
                ('factor', models.FloatField(verbose_name='Factor')),
                ('grade', models.IntegerField(verbose_name='Grado')),
                ('gluten', models.IntegerField(verbose_name='Gluten')),
                ('number_1116A', models.IntegerField(verbose_name='Numero 1116A')),
                ('km', models.IntegerField(verbose_name='Kilometros')),
                ('external_voucher_number', models.IntegerField(verbose_name='Numero Comprobante Externo')),
                ('service_billing_number', models.IntegerField(verbose_name='Numero Factura de Servicios')),
                ('service_billing_date', models.DateField(null=True, verbose_name='Fecha Factura de Servicios')),
                ('service_billing', models.CharField(max_length=50, verbose_name='Factura de Servicios')),
                ('to_date', models.DateField(null=True, verbose_name='Fecha Entrega Hasta')),
                ('observations', models.CharField(max_length=300, verbose_name='Observaciones')),
                ('follow_destination', models.CharField(max_length=2, verbose_name='Sigue a Destino')),
                ('net_weight', models.IntegerField(verbose_name='Peso Neto')),
                ('tare', models.IntegerField(verbose_name='Tara')),
            ],
            options={
                'verbose_name': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='SpeciesHarvest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('movement_type', models.CharField(max_length=1, verbose_name='Tipo Movimiento')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('speciesharvest', models.CharField(max_length=8, null=True, verbose_name='Especie Cosecha')),
                ('species_description', models.CharField(max_length=50, verbose_name='Especie y Cosecha')),
            ],
            options={
                'verbose_name': 'Especies y Cosechas',
            },
        ),
        migrations.CreateModel(
            name='TicketsAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('ticket', models.CharField(max_length=16, verbose_name='Ticket')),
                ('field', models.IntegerField(verbose_name='Campo')),
                ('field_description', models.CharField(max_length=100, verbose_name='Nombre de Campo')),
                ('species', models.CharField(max_length=4, verbose_name='Especie')),
                ('harvest', models.CharField(max_length=4, verbose_name='Cosecha')),
                ('speciesharvest', models.CharField(max_length=8, null=True, verbose_name='Especie Cosecha')),
                ('grade', models.IntegerField(verbose_name='Grado')),
                ('factor', models.FloatField(verbose_name='Factor')),
                ('analysis_costs', models.FloatField(verbose_name='Gastos de Analisis')),
                ('gluten', models.IntegerField(verbose_name='Gluten')),
                ('analysis_item', models.IntegerField(verbose_name='Rubro de Analisis')),
                ('percentage', models.FloatField(verbose_name='Porcentaje')),
                ('bonus', models.FloatField(verbose_name='Bonificacion')),
                ('reduction', models.FloatField(verbose_name='Rebaja')),
                ('item_descripcion', models.CharField(max_length=100, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name': 'Analisis por Ticket',
            },
        ),
        migrations.CreateModel(
            name='ViewedNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.BooleanField(default=False, verbose_name='Notificación vista')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Notifications')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notificación por Usuario',
                'verbose_name_plural': 'Notificaciones por Usuario',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(unique=True, verbose_name='Cuenta Algoritmo')),
                ('company_name', models.CharField(max_length=150, verbose_name='Razón Social')),
                ('is_commercial', models.BooleanField(default=False, verbose_name='Es Comercial?')),
                ('account_confirmed', models.BooleanField(default=False, verbose_name='Cuenta Confirmada?')),
                ('random_password', models.BooleanField(default=True, verbose_name='Password Aleatorio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algoritmo_code', models.IntegerField(verbose_name='Cuenta Algoritmo')),
                ('logged', models.DateTimeField(auto_now_add=True, verbose_name='Fecha/Hora de Ingreso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Log de Acceso',
                'verbose_name_plural': 'Log de Acceso',
            },
        ),
        migrations.CreateModel(
            name='RainDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mm', models.FloatField(verbose_name='Milimetros')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.City', verbose_name='Ciudad')),
                ('rain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Rain', verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Detalle',
                'verbose_name_plural': 'Detalles',
                'unique_together': {('rain', 'city')},
            },
        ),
    ]
