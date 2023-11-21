from django.db import models

class Debts(models.Model):
    id = models.AutoField(primary_key=True) 
    bank = models.CharField(max_length=100)
    value = models.FloatField()
    maturity = models.DateField()

class Budget(models.Model):
    value = models.FloatField()
