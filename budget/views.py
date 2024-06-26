from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction

@api_view(['GET'])
def home(request):
    return Response({"API Version": "1.0.0"})

"""
================
    Débitos
================
"""

@api_view(['POST'])
def create_debt(request):
    data = request.data

    required_fields = ['id_bank', 'value', 'maturity', 'month' ,'id_responsible']

    for field in required_fields:
        if field not in data:
            return Response({f'{field} é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Transforma o valor em um número
        value = float(data['value'])

        # Transforma a data de vencimento no formato correto
        maturity = datetime.strptime(data['maturity'], '%Y-%m-%d').date()

        id_responsible = data['id_responsible']
        responsible = Responsible.objects.get(id=id_responsible)

        id_bank = data['id_bank']
        bank= Bank.objects.get(id=id_bank)

        # Cria a instância de Debts associada ao Responsible
        debt = Debts.objects.create(
            id_bank=bank,
            value=value,
            maturity=maturity,
            month=data['month'],
            id_responsible=responsible
        )
        return Response({'message': 'Débito criado com sucesso'}, status=status.HTTP_201_CREATED)
    
    except Responsible.DoesNotExist:
        return Response({'error': f'Responsável com id {id_responsible} não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    except Bank.DoesNotExist:
        return Response({'error': f'Banco com id {id_bank} não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    except ValueError as error:
        return Response({'error': f'Erro ao criar débito: {str(error)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_debts(request):
    debt_id = request.GET.get('id')

    try:
        if debt_id is not None:
            debt = Debts.objects.get(id=debt_id)
            data = {
                'id': debt.id,
                'value': debt.value,
                'maturity': debt.maturity.strftime('%Y-%m-%d'),
                'month': debt.month,
                'bank': {
                    'id': debt.id_bank.id,
                    'nome': debt.id_bank.name,
                    'cnpj': debt.id_bank.cnpj,
                    'digital_bank': debt.id_bank.digital_bank,
                },
                'responsible' : {
                    'id': debt.id_responsible.id,
                    'name': debt.id_responsible.name
                }
            }
            return JsonResponse(data)
    except Debts.DoesNotExist:
        return Response({'error': f'Débito com id {debt_id} não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    debts = Debts.objects.all()

    data = {
        'debts': [
            {
                'id': debt.id,
                'value': debt.value,
                'maturity': debt.maturity.strftime('%Y-%m-%d'),
                'month':debt.month,
                'bank': {
                    'id': debt.id_bank.id,
                    'nome': debt.id_bank.name,
                    'cnpj': debt.id_bank.cnpj,
                    'digital_bank': debt.id_bank.digital_bank,
                },
                'responsible' : {
                    'id': debt.id_responsible.id,
                    'name': debt.id_responsible.name
                },
            }
            for debt in debts
        ]
    }
    return JsonResponse(data)

@api_view(['PUT'])
def edit_debt(request):
    debt_id = request.GET.get('id')

    if debt_id is None:
        return Response({'result': 'O parâmetro "id" não foi fornecido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        debt = Debts.objects.get(id=debt_id)
        data = request.data

        if 'id_bank' in data:
            bank = Bank.objects.get(id=data['id_bank'])
            debt.id_bank_id = data['id_bank']
        debt.value = data.get('value', debt.value)
        debt.maturity = data.get('maturity', debt.maturity)
        if 'id_responsible' in data:
            responsible = Responsible.objects.get(id=data['id_responsible'])
            debt.id_responsible_id = data['id_responsible']
        debt.month = data.get('month', debt.month)

        debt.save()

        return Response({'result': 'Débito editado com sucesso!'})

    except Debts.DoesNotExist:
        return Response({'result': f'Débito com id {debt_id} não existe!'}, status=status.HTTP_404_NOT_FOUND)
    except Bank.DoesNotExist:
        return Response({'result': 'Banco com o ID fornecido não existe!'}, status=status.HTTP_404_NOT_FOUND)
    except Responsible.DoesNotExist:
        return Response({'result': 'Responsável com o ID fornecido não existe!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({'result': f'Erro na requisição: {str(error)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_debt(request):
    debt_id = request.GET.get('id')

    if debt_id is None:
       return Response({'message': 'O parâmetro "id" não foi fornecido '}, status=status.HTTP_400_BAD_REQUEST)

    try: 
        debt = Debts.objects.get(id=debt_id)
        debt.delete()
        return Response({'message': 'Débito deletado com sucesso'}, status=status.HTTP_200_OK)
    except Debts.DoesNotExist:
        return Response({'message': f'Débito com id {debt_id} naõ encontrado'}, status=status.HTTP_404_NOT_FOUND)

"""
=====================
    Responsaveis
=====================
"""

@api_view(['POST'])
def create_responsibles(request):
    if request.method == 'POST':
        data = request.data

        required_fields = ['name']
        if required_fields[0] not in request.data :
            return Response({f'{required_fields[0]} é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            responsible = Responsible.objects.create(
                name=data['name']
            )
            return Response({'message': 'Responsavel criado com sucesso'}, status=status.HTTP_201_CREATED)

        except ValueError as error:
            return Response({'error': f'Erro ao criar dívida: {str(error)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_responsibles(request):
    responsible_id = request.GET.get('id')

    try:
        if responsible_id is not None:
            responsible = Responsible.objects.get(id=responsible_id)
            data = {
                'id': responsible.id,
                'name': responsible.name
            }
            return JsonResponse(data)
    except Responsible.DoesNotExist:
        return Response({'error': f'Responsável com id {responsible_id} não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    responsibles = Responsible.objects.all()

    data = [
        {
            'id': responsible.id,
            'name': responsible.name
        }
        for responsible in responsibles
    ]

    return JsonResponse(data, safe=False)

@api_view(['PUT'])
def edit_responsibles(request):
    responsible_id = request.GET.get('id')

    try:
        responsible = Responsible.objects.get(id=responsible_id)

        data = request.data

        responsible.name = data.get('name', responsible.name)

        responsible.save()

        result = {'result': f'Responsavel {responsible.name} editado com sucesso!'}

        return Response(result)
    except Bank.DoesNotExist:
        return Response({'result': f'Banco com id {responsible_id} não existe!'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'result': 'Um ou mais paramêtros não foram encontrados na requisição!'}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE'])
def delete_responsibles(request):
    responsible_id = request.GET.get('id')

    if responsible_id is None:
       return Response({'message': 'O parâmetro "id" não foi fornecido '}, status=status.HTTP_400_BAD_REQUEST)

    try:
        responsible = Responsible.objects.get(id=responsible_id)

        responsible.delete()

        return Response({'message': 'Responsável deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
    except Responsible.DoesNotExist:
        return Response({'message': 'Essa dívida não existe'}, status=status.HTTP_400_BAD_REQUEST)

"""
=============
    Bancos
=============
"""

@api_view(['POST'])
def create_bank(request):
    if request.method == 'POST':
        data = request.data

        required_fields = ['name', 'digital_bank']
        for field in required_fields:
            if field not in data:
                Response({'error': f'Campo {field} é obrigatório!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank = Bank.objects.create(
                name = data['name'],
                digital_bank = data['digital_bank']
            )

            return Response({'message': 'Banco adicionado com sucesso!'}, status=status.HTTP_201_CREATED)
        except ValueError as error:
            return Response({'error': f'Erro ao registrar banco: {error}'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_banks(request):
    if request.method == 'GET':
        banks = Bank.objects.all()

        jsonBanks = {
            'banks': [
                {
                    'id': bank.id,
                    'name': bank.name,
                    'cnpj': bank.cnpj,
                    'digital_bank': bank.digital_bank
                }
                for bank in banks
            ]
        }

        return JsonResponse(jsonBanks)
    return Response({'error': f'Método {request.method} não permitido'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_bank(request):
    bank_id = request.GET.get('id')
    try:
        bank = Bank.objects.get(id=bank_id)

        data = request.data

        bank.name = data['name']
        bank.cnpj = data['cnpj']
        bank.digital_bank = data['digital_bank']

        bank.save()

        result = {'result': f'Banco {bank.name} editado com sucesso!'}

        return Response(result)
    except Bank.DoesNotExist:
        return Response({'result': f'Banco com id {bank_id} não existe!'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'result': 'Um ou mais paramêtros não foram encontrados na requisição!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
@api_view(['DELETE'])
def del_bank(request):
    bank_id = request.GET.get('id')

    if bank_id is None:
        return Response({'message': 'O parâmetro "id" não foi fornecido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        bank = Bank.objects.get(id=bank_id)
        bank.delete()

        return Response({'message': f'Banco {bank_id} deletado com sucesso!'}, status=status.HTTP_200_OK)
    except ValueError as error: 
        return Response({'error': f'Erro ao deletar banco: {str(error)}'}, status=status.HTTP_400_BAD_REQUEST)