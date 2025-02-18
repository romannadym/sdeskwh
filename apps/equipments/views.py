from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from equipments.api.api import EquipmentsListAPIView, EquipmentTypesListAPIView, EquipmentVendorsListAPIView, EquipmentBrandsListAPIView, EquipmentModelsListAPIView
from equipments.api.api import GetEquipment, GetEquipmentType, GetEquipmentVendor, GetEquipmentBrand, GetEquipmentModel

from equipments.forms import EquipmentForm, EquipmentDeleteForm, TypeForm, TypeDeleteForm, VendorForm, VendorDeleteForm, BrandForm, BrandDeleteForm, ModelForm, ModelDeleteForm

from admin.forms import ImportForm

#Типы оборудования
@login_required
def TypesListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-types')

    items = EquipmentTypesListAPIView().get(request = request).data
    cols = ['Наименование',]
    links = {
        'add_link': 'add-type',
        'edit_link': 'edit-type',
        'delete_link': 'api-delete-equipment-types',
        'excel_link': 'api-excel-equipment-types',
        'import_link': 'import-types'
    }
    context = {'items': items, 'cols': cols, 'label': 'Справочник "Типы оборудования"', 'links': links, 'link': 'list-types'}

    return render(request, 'admin/list.html', context)

@login_required
def AddTypeView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-types')

    form = TypeForm()
    context = {'form': form, 'action': reverse('api-equipment-types'), 'link': 'list-types'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditTypeView(request, type_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-types')

    item = GetEquipmentType(type_id)
    form = TypeForm(instance = item)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-equipment-types', kwargs = {'type_id': type_id}), 'link': 'list-types', 'delete_link': 'delete-type'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteTypeView(request, type_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-types')

    item = GetEquipmentType(type_id)
    form = TypeDeleteForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-equipment-types', kwargs = {'type_id': type_id}), 'link': 'list-types'}
    return render(request, 'admin/delete.html', context)

@login_required
def ImportTypeView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-types')

    form = ImportForm()

    context = {'form': form, 'files': True, 'action': reverse('api-excel-equipment-types'), 'link': 'list-types'}
    return render(request, 'admin/edit.html', context)

#Вендоры оборудования
@login_required
def VendorListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-vendors')

    items = EquipmentVendorsListAPIView().get(request = request).data
    cols = ['Наименование',]
    links = {
        'add_link': 'add-vendor',
        'edit_link': 'edit-vendor',
        'delete_link': 'api-delete-equipment-vendors',
        'excel_link': 'api-excel-equipment-vendors',
        'import_link': 'import-vendors'
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Вендоры"', 'links': links, 'link': 'list-vendors'}
    return render(request, 'admin/list.html', context)

@login_required
def AddVendorView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-vendors')

    form = VendorForm()

    context = {'form': form, 'action': reverse('api-equipment-vendors'), 'link': 'list-vendors'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditVendorView(request, vendor_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-vendors')

    item = GetEquipmentVendor(vendor_id)
    form = VendorForm(instance = item)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-equipment-vendors', kwargs = {'vendor_id': vendor_id}), 'link': 'list-vendors', 'delete_link': 'delete-vendor'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteVendorView(request, vendor_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-vendors')

    item = GetEquipmentVendor(vendor_id)
    form = VendorDeleteForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-equipment-vendors', kwargs = {'vendor_id': vendor_id}), 'link': 'list-vendors'}
    return render(request, 'admin/delete.html', context)

@login_required
def ImportVendorsView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-vendors')

    form = ImportForm()

    context = {'form': form, 'files': True, 'action': reverse('api-excel-equipment-vendors'), 'link': 'list-vendors'}
    return render(request, 'admin/edit.html', context)

#Бренды оборудования
@login_required
def BrandListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-brands')

    items = EquipmentBrandsListAPIView().get(request = request).data
    cols = ['Наименование',]
    links = {
        'add_link': 'add-brand',
        'edit_link': 'edit-brand',
        'delete_link': 'api-delete-equipment-brands',
        'excel_link': 'api-excel-equipment-brands',
        'import_link': 'import-brands'
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Бренды"', 'links': links}
    return render(request, 'admin/list.html', context)

@login_required
def AddBrandView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-brands')

    form = BrandForm()

    context = {'form': form, 'action': reverse('api-equipment-brands'), 'link': 'list-brands'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditBrandView(request, brand_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-brands')

    item = GetEquipmentBrand(brand_id)
    form = BrandForm(instance = item)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-equipment-brands', kwargs = {'brand_id': brand_id}), 'link': 'list-brands', 'delete_link': 'delete-brand'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteBrandView(request, brand_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-brands')

    item = GetEquipmentBrand(brand_id)
    form = BrandDeleteForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-equipment-brands', kwargs = {'brand_id': brand_id}), 'link': 'list-brands'}
    return render(request, 'admin/delete.html', context)

@login_required
def ImportBrandsView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-brands')

    form = ImportForm()

    context = {'form': form, 'files': True, 'action': reverse('api-excel-equipment-brands'), 'link': 'list-brands'}
    return render(request, 'admin/edit.html', context)

#Модели оборудования
@login_required
def ModelListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-models')

    items = EquipmentModelsListAPIView().get(request = request).data
    cols = ['Наименование', 'Бренд', 'Вендор']
    links = {
        'add_link': 'add-model',
        'edit_link': 'edit-model',
        'delete_link': 'api-delete-equipment-models',
        'excel_link': 'api-excel-equipment-models',
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Модели"', 'links': links, 'link': 'list-models'}
    return render(request, 'admin/list.html', context)

@login_required
def AddModelView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-models')

    form = ModelForm()

    context = {'form': form, 'action': reverse('api-equipment-models'), 'link': 'list-models'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditModelView(request, model_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-models')

    item = GetEquipmentModel(model_id)
    form = ModelForm(instance = item)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-equipment-models', kwargs = {'model_id': model_id}), 'link': 'list-models', 'delete_link': 'delete-model'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteModelView(request, model_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-models')

    item = GetEquipmentModel(model_id)
    form = ModelDeleteForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-equipment-models', kwargs = {'model_id': model_id}), 'link': 'list-models'}
    return render(request, 'admin/delete.html', context)

@login_required
def EquipmentsListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-equipments')

    items = EquipmentsListAPIView().get(request = request).data
    cols = ['Тип', 'Вендор', 'Бренд', 'Модель',]
    links = {
        'add_link': 'add-equipment',
        'edit_link': 'edit-equipment',
        'delete_link': 'api-delete-equipments',
    }
    context = {'items': items, 'cols': cols, 'label': 'Оборудование', 'links': links}

    return render(request, 'admin/list.html', context)

@login_required
def AddEquipmentView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-equipments')

    form = EquipmentForm()

    context = {'form': form, 'search': True, 'action': reverse('api-list-equipments'), 'link': 'list-equipments'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditEquipmentView(request, equipment_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-equipments')

    equipment = GetEquipment(equipment_id)
    form = EquipmentForm(instance = equipment)

    context = {'form': form, 'search': True, 'method': 'PUT', 'action': reverse('api-edit-equipment', kwargs = {'equipment_id': equipment_id}), 'link': 'list-equipments', 'delete_link': 'delete-equipment'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteEquipmentView(request, equipment_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-equipments')

    equipment = GetEquipment(equipment_id)
    form = EquipmentDeleteForm(instance = equipment)

    context = {'form': form, 'action': reverse('api-edit-equipment', kwargs = {'equipment_id': equipment_id}), 'link': 'list-equipments'}
    return render(request, 'admin/delete.html', context)
