# Generated by Django 4.2.7 on 2023-11-30 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_remove_debts_bank_debts_id_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debts',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='debts',
            name='id_bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.bank'),
        ),
    ]
