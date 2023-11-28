from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from datetime import datetime
from django.http import JsonResponse

@api_view(['GET'])
def home(request):
    return Response({"API Version": "1.0.0"})

@api_view(['POST'])
def create_debt(request):
    if request.method == 'POST':
        data = request.data

        required_fields = ['bank', 'value', 'maturity', 'id_responsible']
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

            # Cria a instância de Debts associada ao Responsible
            debt = Debts.objects.create(
                bank=data['bank'],
                value=value,
                maturity=maturity,
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
                'bank': debt.bank,
                'value': debt.value,
                'maturity': debt.maturity.strftime('%Y-%m-%d'),
                'id_responsible': debt.id_responsible.id,

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

        required_fields = [ 'name' ]
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
        

