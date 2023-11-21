# Generated by Django 4.2.4 on 2023-11-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Debts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bank', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('maturity', models.DateField()),
            ],
        ),
    ]
