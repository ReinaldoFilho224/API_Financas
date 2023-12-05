from django.urls import path
from .views import *

urlpatterns = [
    #Debito
    path('create_debt/', create_debt, name='create_debt'),
    path('get_debts/', get_debts, name='get_debts'),
    path('edit_debt/', edit_debt, name='delete_debt'),
    path('delete_debt/', delete_debt, name='delete_debt'),
    
    #Responsaveis
    path('createResponsible/', create_responsibles, name='create_responsible'),
    path('getResponsibles/', get_responsibles, name='getResponsibles'),
    path('editResponsibles/', edit_responsibles, name='editResponsibles'),
    path('deleteResponsibles/', delete_responsibles, name='deleteResponsibles'),

    #Banco
    path('createBank/', create_bank, name='create_bank'),
    path('getBanks/', get_banks, name='get_banks'),
    path('editBank/', edit_bank, name='edit_bank'),
    path('delBank/', del_bank, name='del_bank')
]