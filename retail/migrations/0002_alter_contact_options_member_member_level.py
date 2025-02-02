# Generated by Django 5.1.5 on 2025-01-20 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={
                'ordering': ['-updated_at'],
                'verbose_name': 'контакт',
                'verbose_name_plural': 'контакты',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='member_level',
            field=models.PositiveSmallIntegerField(
                default=0, editable=False, verbose_name='уровень'
            ),
            preserve_default=False,
        ),
    ]
