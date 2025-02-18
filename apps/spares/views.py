from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from spares.api.api import SparesListAdminAPIView, PartNumberListAPIView
from spares.api.api import GetSpare, GetPartNumber

from spares.forms import SpareForm, SparePNFormset, SpareDeleteForm, PartNumberForm, PartNumberDeleteForm

from admin.forms import ImportForm

@login_required
def PartNumbersListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-pn')

    pns = PartNumberListAPIView().get(request = request).data
    cols = ['Партномер',]
    links = {
        'add_link': 'add-pn',
        'edit_link': 'edit-pn',
        'delete_link': 'api-delete-partnumbers',
        'excel_link': 'api-excel-partnumbers',
        'import_link': 'import-partnumbers'
    }

    context = {'items': pns, 'cols': cols, 'label': 'Справочник "Партномера"', 'links': links, 'link': 'list-pn'}
    return render(request, 'admin/list.html', context)

@login_required
def AddPartNumberView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-pn')

    form = PartNumberForm()
    context = {'form': form, 'action': reverse('api-partnumbers'), 'link': 'list-pn'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditPartNumberView(request, pn_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-pn')

    pn = GetPartNumber(pn_id)
    form = PartNumberForm(instance = pn)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-partnumbers', kwargs = {'pn_id': pn_id}), 'link': 'list-pn', 'delete_link': 'delete-pn'}
    return render(request, 'admin/edit.html', context)

@login_required
def DeletePartNumberView(request, pn_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-pn')

    pn = GetPartNumber(pn_id)
    form = PartNumberDeleteForm(instance = pn)

    context = {'form': form, 'action': reverse('api-edit-partnumbers', kwargs = {'pn_id': pn_id}), 'link': 'list-pn'}
    return render(request, 'admin/delete.html', context)

@login_required
def ImportPartNumberView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-pn')

    form = ImportForm()

    context = {'form': form, 'files': True, 'action': reverse('api-excel-partnumbers'), 'link': 'list-pn'}
    return render(request, 'admin/edit.html', context)

@login_required
def SparesListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-spares')

    items = SparesListAdminAPIView().get(request = request).data
    cols = ['Наименование', 'Серийный номер', 'Описание', 'Партномер']
    links = {
        'add_link': 'add-spare',
        'edit_link': 'edit-spare',
        'delete_link': 'api-delete-spares',
        'excel_link': 'api-excel-spares',
        'import_link': 'import-spare'
    }

    context = {'items': items, 'cols': cols, 'label': 'ЗИП', 'links': links, 'link': 'list-spares'}

    return render(request, 'admin/list.html', context)

@login_required
def AddSpareView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-spares')

    form = SpareForm()
    formset = SparePNFormset()

    if request.method == 'POST':
        form = SpareForm(request.POST)
        if form.is_valid():
            spare = form.save(commit = False)
            formset = SparePNFormset(request.POST, instance = spare)
            if formset.is_valid():
                spare.save()
                formset.save()
            return redirect('list-spares')

    formsets = [
        {'formset': formset, 'label': 'Партномера ЗИП'}
    ]

    context = {'form': form, 'formsets': formsets, 'search': True, 'link': 'list-spares'}
    return render(request, 'admin/edit_formset.html', context)

@login_required
def EditSpareView(request, spare_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-spares')

    spare = GetSpare(spare_id)
    form = SpareForm(instance = spare)
    formset = SparePNFormset(instance = spare)

    if request.method == 'POST':
        form = SpareForm(request.POST, instance = spare)
        if form.is_valid():
            spare = form.save(commit = False)
            formset = SparePNFormset(request.POST, instance = spare)
            if formset.is_valid():
                spare.save()
                formset.save()
            return redirect('list-spares')

    formsets = [
        {'formset': formset, 'label': 'Партномера ЗИП'}
    ]

    context = {'form': form, 'formsets': formsets, 'search': True, 'link': 'list-spares', 'delete_link': 'delete-spare'}
    return render(request, 'admin/edit_formset.html', context)

@login_required
def DeleteSpareView(request, spare_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-spares')

    spare = GetSpare(spare_id)
    form = SpareDeleteForm(instance = spare)

    context = {'form': form, 'action': reverse('api-edit-spare', kwargs = {'spare_id': spare_id}), 'link': 'list-spares'}
    return render(request, 'admin/delete.html', context)

@login_required
def ImportView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-spares')

    form = ImportForm()

    context = {'form': form, 'files': True, 'action': reverse('api-excel-spares'), 'link': 'list-spares'}
    return render(request, 'admin/edit.html', context)
