from django.urls import path
from equipments.views import TypesListView, AddTypeView, EditTypeView, DeleteTypeView, ImportTypeView
from equipments.views import VendorListView, AddVendorView, EditVendorView, DeleteVendorView, ImportVendorsView
from equipments.views import BrandListView, AddBrandView, EditBrandView, DeleteBrandView, ImportBrandsView
from equipments.views import ModelListView, AddModelView, EditModelView, DeleteModelView
from equipments.views import EquipmentsListView, AddEquipmentView, EditEquipmentView, DeleteEquipmentView

from equipments.api.api import EquipmentsListAPIView, EditEquipmentAPIView, EquipmentsDeleteAPIView
from equipments.api.api import EquipmentTypesListAPIView, EditEquipmentTypeAPIView, EquipmentTypesDeleteAPIView, EquipmentTypesExcelAPIView
from equipments.api.api import EquipmentVendorsListAPIView, EditEquipmentVendorAPIView, EquipmentVendorsDeleteAPIView, EquipmentVendorsExcelAPIView
from equipments.api.api import EquipmentBrandsListAPIView, EditEquipmentBrandAPIView, EquipmentBrandsDeleteAPIView, EquipmentBrandsExcelAPIView
from equipments.api.api import EquipmentModelsListAPIView, EditEquipmentModelAPIView, EquipmentModelsDeleteAPIView, EquipmentModelsExcelAPIView

urlpatterns = [
    path('types/', TypesListView, name = 'list-types'),
    path('types/add/', AddTypeView, name = 'add-type'),
    path('types/edit/<int:type_id>', EditTypeView, name = 'edit-type'),
    path('types/delete/<int:type_id>', DeleteTypeView, name = 'delete-type'),
    path('types/import/', ImportTypeView, name = 'import-types'),

    path('vendors/', VendorListView, name = 'list-vendors'),
    path('vendors/add/', AddVendorView, name = 'add-vendor'),
    path('vendors/edit/<int:vendor_id>', EditVendorView, name = 'edit-vendor'),
    path('vendors/delete/<int:vendor_id>', DeleteVendorView, name = 'delete-vendor'),
    path('vendors/import/', ImportVendorsView, name = 'import-vendors'),

    path('brands/', BrandListView, name = 'list-brands'),
    path('brands/add/', AddBrandView, name = 'add-brand'),
    path('brands/edit/<int:brand_id>', EditBrandView, name = 'edit-brand'),
    path('brands/delete/<int:brand_id>', DeleteBrandView, name = 'delete-brand'),
    path('brands/import/', ImportBrandsView, name = 'import-brands'),

    path('models/', ModelListView, name = 'list-models'),
    path('models/add/', AddModelView, name = 'add-model'),
    path('models/edit/<int:model_id>', EditModelView, name = 'edit-model'),
    path('models/delete/<int:model_id>', DeleteModelView, name = 'delete-model'),

    path('equipments/', EquipmentsListView, name = 'list-equipments'),
    path('add_equipment/', AddEquipmentView, name = 'add-equipment'),
    path('edit_equipment/<int:equipment_id>', EditEquipmentView, name = 'edit-equipment'),
    path('delete_equipment/<int:equipment_id>', DeleteEquipmentView, name = 'delete-equipment'),

    path('api/list/', EquipmentsListAPIView.as_view(), name = 'api-list-equipments'),
    path('api/edit/<int:equipment_id>', EditEquipmentAPIView.as_view(), name = 'api-edit-equipment'),
    path('api/delete/', EquipmentsDeleteAPIView.as_view(), name = 'api-delete-equipments'),

    path('api/types/', EquipmentTypesListAPIView.as_view(), name = 'api-equipment-types'),
    path('api/types/edit/<int:type_id>', EditEquipmentTypeAPIView.as_view(), name = 'api-edit-equipment-types'),
    path('api/types/delete/', EquipmentTypesDeleteAPIView.as_view(), name = 'api-delete-equipment-types'),
    path('api/types/excel/', EquipmentTypesExcelAPIView.as_view(), name = 'api-excel-equipment-types'),

    path('api/vendors/', EquipmentVendorsListAPIView.as_view(), name = 'api-equipment-vendors'),
    path('api/vendors/edit/<int:vendor_id>', EditEquipmentVendorAPIView.as_view(), name = 'api-edit-equipment-vendors'),
    path('api/vendors/delete/', EquipmentVendorsDeleteAPIView.as_view(), name = 'api-delete-equipment-vendors'),
    path('api/vendors/excel/', EquipmentVendorsExcelAPIView.as_view(), name = 'api-excel-equipment-vendors'),

    path('api/brands/', EquipmentBrandsListAPIView.as_view(), name = 'api-equipment-brands'),
    path('api/brands/edit/<int:brand_id>', EditEquipmentBrandAPIView.as_view(), name = 'api-edit-equipment-brands'),
    path('api/brands/delete/', EquipmentBrandsDeleteAPIView.as_view(), name = 'api-delete-equipment-brands'),
    path('api/brands/excel/', EquipmentBrandsExcelAPIView.as_view(), name = 'api-excel-equipment-brands'),

    path('api/models/', EquipmentModelsListAPIView.as_view(), name = 'api-equipment-models'),
    path('api/models/edit/<int:model_id>', EditEquipmentModelAPIView.as_view(), name = 'api-edit-equipment-models'),
    path('api/models/delete/', EquipmentModelsDeleteAPIView.as_view(), name = 'api-delete-equipment-models'),
    path('api/models/excel/', EquipmentModelsExcelAPIView.as_view(), name = 'api-excel-equipment-models'),
]
