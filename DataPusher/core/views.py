
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationListCreate(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        return Destination.objects.filter(account_id=self.kwargs['account_id'])

class DestinationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class AccountDestinations(APIView):
    def get(self, request, account_id):
        destinations = Destination.objects.filter(account_id=account_id)
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

class DataHandler(APIView):
    def post(self, request):
        token = request.headers.get('CL-X-TOKEN')
        if not token:
            return Response({'message': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            account = Account.objects.get(app_secret_token=token)
        except Account.DoesNotExist:
            return Response({'message': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        for destination in account.destinations.all():
            headers = destination.headers
            method = destination.http_method
            url = destination.url

            if method == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)

            if response.status_code != 200:
                return Response({'message': 'Failed to send data to some destinations'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Data sent successfully'})
