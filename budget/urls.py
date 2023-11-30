from django.urls import path
from .views import *

urlpatterns = [
    path('create_debt/', create_debt, name='create_debt'),
    path('get_debts/', get_debts, name='get_debts'),
    path('delete_debt/<int:id>/', delete_debt, name='delete_debt'),
    
    #Responsaveis
    path('createResponsible/', create_responsibles, name='create_responsible'),

    #Banco
    path('createBank/', create_bank, name='create_bank'),
    path('getBanks/', get_banks, name='get_banks')
]