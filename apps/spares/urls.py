from django.urls import path
from spares.views import PartNumbersListView, AddPartNumberView, EditPartNumberView, DeletePartNumberView, ImportPartNumberView
from spares.views import SparesListView, AddSpareView, EditSpareView, DeleteSpareView, ImportView

from spares.api.api import SparesListAPIView, SparesListAdminAPIView, SparesExcelAPIView, SpareEditAPIView, SparesDeleteAPIView
from spares.api.api import PartNumberListAPIView, PartNumberEditAPIView, PartNumbersDeleteAPIView, PartNumbersExcelAPIView

urlpatterns = [
    path('pns/', PartNumbersListView, name = 'list-pn'),
    path('pns/add/', AddPartNumberView, name = 'add-pn'),
    path('pns/edit/<int:pn_id>', EditPartNumberView, name = 'edit-pn'),
    path('pns/delete/<int:pn_id>', DeletePartNumberView, name = 'delete-pn'),

    path('pns/import/', ImportPartNumberView, name = 'import-partnumbers'),

    path('spares/', SparesListView, name = 'list-spares'),
    path('add_spare/', AddSpareView, name = 'add-spare'),
    path('edit_spare/<int:spare_id>', EditSpareView, name = 'edit-spare'),
    path('delete_spare/<int:spare_id>', DeleteSpareView, name = 'delete-spare'),

    path('import_spare/', ImportView, name = 'import-spare'),

    path('api/list/', SparesListAPIView.as_view()),
    path('api/admin/list/', SparesListAdminAPIView.as_view(), name = 'api-spares'),
    path('api/admin/excel/', SparesExcelAPIView.as_view(), name = 'api-excel-spares'),
    path('api/edit/<int:spare_id>', SpareEditAPIView.as_view(), name = 'api-edit-spare'),
    path('api/delete/', SparesDeleteAPIView.as_view(), name = 'api-delete-spares'),

    path('api/pns/', PartNumberListAPIView.as_view(), name = 'api-partnumbers'),
    path('api/pns/edit/<int:pn_id>', PartNumberEditAPIView.as_view(), name = 'api-edit-partnumbers'),
    path('api/pns/delete/', PartNumbersDeleteAPIView.as_view(), name = 'api-delete-partnumbers'),
    path('api/pns/excel/', PartNumbersExcelAPIView.as_view(), name = 'api-excel-partnumbers'),
]
