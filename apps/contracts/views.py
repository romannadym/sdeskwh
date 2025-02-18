from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from contracts.api.api import SupportLevelsListAPIView, SupportLevelEditAPIView
from contracts.api.api import ContractsListAPIView
from contracts.api.api import GetSupportLevel, GetContract

from contracts.forms import LevelForm, LevelDeleteForm, ContractForm, EquipmentForm, EquipmentFormset, ContractDeleteForm

@login_required
def SupportLevelsListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-levels')

    items = SupportLevelsListAPIView.as_view()(request = request).data
    cols = ['Наименование',]

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Тип поддержи"', 'add_link': 'add-level', 'edit_link': 'edit-level', 'model': 'SupportLevelModel'}

    return render(request, 'admin/list.html', context)

@login_required
def AddSupportLevelView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-levels')

    form = LevelForm()

    context = {'form': form, 'action': reverse('list-levels-api'), 'link': 'list-levels'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditSupportLevelView(request, level_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-levels')

    form = LevelForm(instance = GetSupportLevel(level_id))

    context = {'form': form, 'method': 'PUT', 'action': reverse('edit-level-api', kwargs = {'level_id': level_id}), 'link': 'list-levels', 'delete_link': 'delete-level'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeleteSupportLevelView(request, level_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-levels')

    form = LevelDeleteForm(instance = GetSupportLevel(level_id))

    context = {'form': form, 'action': reverse('edit-level-api', kwargs = {'level_id': level_id}), 'link': 'list-levels'}
    return render(request, 'admin/delete.html', context)

@login_required
def ContractsListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-contracts')

    items = ContractsListAPIView.as_view()(request = request).data
    cols = ['Номер договора', 'Поставщик',]
    links = {
        'add_link': 'add-contract',
        'edit_link': 'edit-contract',
        'delete_link': 'contracts-delete-api',
    }

    context = {'items': items, 'cols': cols, 'label': 'Контракты', 'links': links}

    return render(request, 'admin/list.html', context)

@login_required
def AddContractView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-contracts')

    form = ContractForm()
    formset = EquipmentFormset()

    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit = False)
            formset = EquipmentFormset(request.POST, instance = contract)
            if formset.is_valid():
                contract.save()
                formset.save()
            return redirect('list-contracts')

    formsets = [
        {'formset': formset, 'label': 'Оборудование'},
    ]

    context = {'form': form, 'formsets': formsets, 'search': True, 'dates': True, 'action': reverse('list-contracts-api'), 'link': 'list-contracts'}
    return render(request, 'admin/edit_formset.html', context)

@login_required
def EditContractView(request, contract_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-contracts')

    contract = GetContract(contract_id)
    form = ContractForm(instance = contract)
    formset = EquipmentFormset(instance = contract)

    if request.method == 'POST':
        form = ContractForm(request.POST, instance = contract)
        if form.is_valid():
            contract = form.save(commit = False)
            formset = EquipmentFormset(request.POST, instance = contract)
            if formset.is_valid():
                contract.save()
                formset.save()
            return redirect('list-contracts')

    formsets = [
        {'formset': formset, 'label': 'Оборудование'},
    ]

    context = {'form': form, 'formsets': formsets, 'search': True, 'dates': True, 'link': 'list-contracts', 'delete_link': 'delete-contract'}
    return render(request, 'admin/edit_formset.html', context)

@login_required
def DeleteContractView(request, contract_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-contracts')

    contract = GetContract(contract_id)
    form = ContractDeleteForm(instance = contract)

    context = {'form': form, 'action': reverse('edit-contracts-api', kwargs = {'contract_id': contract_id}), 'link': 'list-contracts'}
    return render(request, 'admin/delete.html', context)
