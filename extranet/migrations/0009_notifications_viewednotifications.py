# Generated by Django 3.0.12 on 2023-09-13 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extranet', '0008_userinfo'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
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
            ],
            # Table already exists. See website/migrations/0017_auto_20230913_0113.py
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='ViewedNotifications',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('viewed', models.BooleanField(default=False, verbose_name='Notificación vista')),
                        ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extranet.Notifications')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'verbose_name': 'Notificación por Usuario',
                        'verbose_name_plural': 'Notificaciones por Usuario',
                    },
                ),
            ],
            # Table already exists. See website/migrations/0017_auto_20230913_0113.py
            database_operations=[],
        ),
    ]
