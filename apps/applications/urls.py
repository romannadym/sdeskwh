from django.urls import path
from applications.views import AddApplicationView, EqModelsView, DetailsApplicationView, EquipmentExcelView, AllEquipmentExcelView
from applications.views import EditApplicationView, TestTaskView, SnEqView, ApplicationHistoryView, SpareExcelView, GetOrganizationView
from applications.views import GetContactsView, SpareLoadView
from applications.views import GetSpareModels, GetModelPNs, GetSparesList, InstalledBaseExcel, GetEquipmentsInEdit, ReadingEmailSelver
from applications.views import ListApplicationView, NewAddApplicationView, TestView, EditCommentView, DeleteCommentView
# , ListApplicationView
from applications.api.api import *

urlpatterns = [
    path('add/', AddApplicationView, name = 'add-application'),
    path('edit/<int:application_id>', EditApplicationView, name = 'edit-application'),
    path('models/', EqModelsView, name = 'models'),
    path('details/<int:application_id>', DetailsApplicationView, name = 'app-details'),
    path('history/<int:application_id>/<int:type>', ApplicationHistoryView, name = 'app-history'),
    # path('logs/<int:application_id>', ApplicationLogsView, name = 'app-logs'),
    path('comment/edit/<int:comment_id>/<int:link_type>', EditCommentView, name = 'edit-comment'),
    path('comment/delete/<int:comment_id>/<int:link_type>', DeleteCommentView, name = 'delete-comment'),
    # path('list/', ListApplicationView, name = 'app-list'),
    # path('sn_eqs/<str:sn>', SnEqView, name = 'sn-eqs'),
    path('eq_excel/', EquipmentExcelView, name = 'eq-excel'),
    path('all_eq_excel/', AllEquipmentExcelView, name = 'all-eq-excel'),
    path('installed_base/', InstalledBaseExcel, name = 'installed-base'),
    path('spare_models/', GetSpareModels, name = 'spare-models'),
    path('model_pns/', GetModelPNs, name = 'model-pns'),
    path('spare_excel/', SpareExcelView, name = 'spare-excel'),
    path('spare_load/', SpareLoadView, name = 'spare-load'),
    path('get_organization/', GetOrganizationView, name = 'get-organization'),
    path('get_spares_list/', GetSparesList, name = 'get-spares-list'),
    path('get_contacts/', GetContactsView, name = 'get-contacts'),
    path('get_eqs_in_edit/', GetEquipmentsInEdit, name = 'get-eqs-in-edit'),

    path('read_emails/', ReadingEmailSelver, name = 'read-emails'),
    # path('test_task/', TestTaskView, name = 'test-task'),

    path('apps_list/', ListApplicationView, name = 'app-list'),
    # path('new_add/', NewAddApplicationView, name = 'new-add-application'),

    # path('test/', TestView),

    path('api/app_priorities/', AppPrioritiesListAPIView.as_view()),
    path('api/app_statuses/', AppStatusesAPIView.as_view()),
    path('api/clients_equipments/<int:client_id>', GetClientsEquipmentsAPIView.as_view()),

    path('api/list/', ApplicationsListAPIView.as_view(), name = 'applications-list'),
    path('api/clients_contacts/<int:client_id>', GetClientsContactsAPIView.as_view()),
    path('api/add/', AddApplicationAPIView.as_view(), name = 'add-application-api'),
    path('api/list_to_excel/', ApplicationsExcelAPIView.as_view(), name = 'applications-to-excel'),
    path('api/edit/<int:application_id>', EditApplicationAPIView.as_view(), name = 'edit-application-api'),
    path('api/edit/<int:application_id>/<int:status_id>', EditDoneApplicationAPIView.as_view(), name = 'edit-done-application-api'),
    path('api/edit/documents/<int:application_id>', ApplicationDocumentsAPIView.as_view(), name = 'add-app-docs-api'),
    path('api/edit/comments/<int:application_id>', ApplicationCommentsAPIView.as_view(), name = 'add-app-comm-api'),
    path('api/comment/<int:comment_id>', AppCommentAPIView.as_view(), name = 'edit-app-comm-api'),
    path('api/history/<int:application_id>', ApplicationHistoryAPIView.as_view()),
    path('api/logs/<int:application_id>', ApplicationLogsAPIView.as_view()),
    path('api/spares/<int:application_id>', AppSpareAPIView.as_view(), name = 'add-app-spare-api'),

    path('api/client/contracts/', GetClientsContractsAPIView.as_view(), name = 'clients-contracts-api'),
    path('api/client/contracts/excel/', ClientsContractsExcelAPIView.as_view(), name = 'clients-contracts-excel-api'),

    path('api/details/<int:application_id>', ApplicationDetailsAPIView.as_view(), name = 'app-details-api'),
]
