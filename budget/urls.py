from django.urls import path
from .views import *

urlpatterns = [
    path('create_debt/', create_debt, name='create_debt'),
    path('get_debts/', get_debts, name='get_debts'),
    
    #Responsaveis
    path('createResponsible/', create_responsibles, name='create_responsible')
]