from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def home(request):
    return Response({"API Version": "1.0.0"})


@api_view(['POST'])
def create_debt(request):
    if request.method == 'POST':
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

            # Certifica-se de que o Responsible com o ID fornecido existe
            id_responsible = data['id_responsible']
            responsible = Responsible.objects.get(id=id_responsible)

            # Certifica-se de que o Responsible com o ID fornecido exist
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

            return Response({'message': 'Dívida criada com sucesso'}, status=status.HTTP_201_CREATED)

        except Responsible.DoesNotExist:
            return Response({'error': 'Responsável não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({'error': f'Erro ao criar dívida: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_debts(request):
    # Consulta o banco de dados para obter todas as dívidas
    debts = Debts.objects.all()

    # Retorna os dados diretamente como JSON
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
        ],
    }
    return JsonResponse(data)

#Responsaveis

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

        except ValueError as e:
                # Se ocorrer um erro ao criar a dívida, envia uma resposta de erro
                return Response({'error': f'Erro ao criar dívida: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # for field in required_fields:
        #     if field not in data:
        #         return Response({f'{field} é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['DELETE'])
def delete_debt(request, id):
    if request.method == 'DELETE':
        try: 
            debt = Debts.objects.get(id=id)
            # Deleta a instância da dívida
            debt.delete()
            return Response({'message': 'Dívida deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Debts.DoesNotExist:
            return Response({'message': 'Essa dívida não existe'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_bank(request):
    if request.method == 'POST':
        data = request.data

        required_fields = ['name', 'cnpj', 'digital_bank']
        for field in required_fields:
            if field not in data:
                Response({'error': f'Campo {field} é obrigatório!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank = Bank.objects.create(
                name = data['name'],
                cnpj = data['cnpj'],
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