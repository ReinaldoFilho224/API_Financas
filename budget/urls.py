from django.urls import path
from .views import create_debt, get_debts

urlpatterns = [
    path('create-debt/', create_debt, name='create_debt'),
    path('get-debts/', get_debts, name='get_debts'),
]