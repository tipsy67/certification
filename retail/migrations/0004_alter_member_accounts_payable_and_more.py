# Generated by Django 5.1.5 on 2025-01-20 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0003_alter_member_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='accounts_payable',
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=15, verbose_name='кредиторка'
            ),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_level',
            field=models.PositiveSmallIntegerField(
                default=0, editable=False, verbose_name='уровень'
            ),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_type',
            field=models.CharField(
                choices=[
                    ('PLNT', 'Завод'),
                    ('INDV', 'Индивидуальный предприниматель'),
                    ('RTL', 'Розничная сеть'),
                ],
                max_length=4,
                verbose_name='тип звена',
            ),
        ),
        migrations.AlterField(
            model_name='member',
            name='supplier',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='retail.member',
                verbose_name='поставщик',
            ),
        ),
    ]
