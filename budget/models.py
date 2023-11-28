from django.db import models

class Responsible(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
class Debts(models.Model):
    id = models.AutoField(primary_key=True) 
    bank = models.CharField(max_length=100)
    value = models.FloatField()
    maturity = models.DateField()
    id_responsible = models.ForeignKey(Responsible, on_delete=models.CASCADE)

class Budget(models.Model):
    value = models.FloatField()


