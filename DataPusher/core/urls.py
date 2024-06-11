from django.urls import path
from .views import AccountListCreate, AccountRetrieveUpdateDestroy, DestinationListCreate, DestinationRetrieveUpdateDestroy, AccountDestinations, DataHandler

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('accounts/<pk>/', AccountRetrieveUpdateDestroy.as_view(), name='account-retrieve-update-destroy'),
    path('accounts/<account_id>/destinations/', DestinationListCreate.as_view(), name='destination-list-create'),
    path('destinations/<pk>/', DestinationRetrieveUpdateDestroy.as_view(), name='destination-retrieve-update-destroy'),
    path('accounts/<account_id>/destinations/list/', AccountDestinations.as_view(), name='account-destinations'),
    path('server/incoming_data/', DataHandler.as_view(), name='incoming-data'),
]