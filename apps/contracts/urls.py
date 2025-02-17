from django.urls import path
from contracts.views import SupportLevelsListView, AddSupportLevelView, EditSupportLevelView, DeleteSupportLevelView
from contracts.views import ContractsListView, AddContractView, EditContractView, DeleteContractView

from contracts.api.api import SupportLevelsListAPIView, SupportLevelEditAPIView
from contracts.api.api import ContractsListAPIView, ContractsEditAPIView, ContractsDeleteAPIView

urlpatterns = [
    path('levels/', SupportLevelsListView, name = 'list-levels'),
    path('add_level/', AddSupportLevelView, name = 'add-level'),
    path('edit_level/<int:level_id>', EditSupportLevelView, name = 'edit-level'),
    path('delete_level/<int:level_id>', DeleteSupportLevelView, name = 'delete-level'),

    path('contracts/', ContractsListView, name = 'list-contracts'),
    path('add_contract/', AddContractView, name = 'add-contract'),
    path('edit_contract/<int:contract_id>', EditContractView, name = 'edit-contract'),
    path('delete_contract/<int:contract_id>', DeleteContractView, name = 'delete-contract'),

    path('api/levels/', SupportLevelsListAPIView.as_view(), name = 'list-levels-api'),
    path('api/levels/<int:level_id>', SupportLevelEditAPIView.as_view(), name = 'edit-level-api'),

    path('api/contracts/', ContractsListAPIView.as_view(), name = 'list-contracts-api'),
    path('api/contracts/<int:contract_id>', ContractsEditAPIView.as_view(), name = 'edit-contracts-api'),
    path('api/contracts/delete/', ContractsDeleteAPIView.as_view(), name = 'contracts-delete-api'),
]
