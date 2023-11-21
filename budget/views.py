from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .serializers import DebtsSerializer
from .models import Debts

@api_view(['POST'])
def create_debt(request):
    if request.method == 'POST':
        data = request.data
        serializer = DebtsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response('Debito criado com sucesso',status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            }
            for debt in debts
        ],
    }

    # Retorna a resposta como JSON
    return JsonResponse(data)

