from rest_framework import serializers
from .models import Debts

class DebtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debts
        fields = ['id', 'bank', 'value', 'maturity']