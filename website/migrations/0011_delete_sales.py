# Generated by Django 3.0.12 on 2023-09-13 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_delete_deliveries'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Sales',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Sales',
                    table='extranet_sales',
                ),
            ],
        )
    ]
