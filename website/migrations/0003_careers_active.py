# Generated by Django 3.0.8 on 2020-08-27 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_careers'),
    ]

    operations = [
        migrations.AddField(
            model_name='careers',
            name='active',
            field=models.BooleanField(default=1, verbose_name='Activo / Inactivo'),
            preserve_default=False,
        ),
    ]
