# Generated by Django 4.2.16 on 2025-03-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalfinance', '0002_alter_pot_target_alter_pot_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
    ]
