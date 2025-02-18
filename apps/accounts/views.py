from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from accounts.api.api import UsersListAPIView, ContactsListAPIView, OrganizationsListAPIView, GroupsListAPIView, GroupsListUserAPIView
from accounts.api.api import PermissionsListAPIView, PermissionsListGroupAPIView
from accounts.api.api import GetUser, GetGroup, GetContact, GetOrganization

from accounts.forms import AddUserForm, EditUserForm, DeleteUserForm, UserGroupForm, DeleteUserGroupForm
from accounts.forms import OrganizationContactForm, OrganizationForm, ContactForm, OrganizationDeleteForm

@login_required
def UserListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-user')

    items = UsersListAPIView().get(request = request).data
    cols = ['Адрес электронной почты', 'Организация', 'Телефон', '', 'Роли']
    links = {
        'add_link': 'add-user',
        'edit_link': 'edit-user',
        'delete_link': 'api-delete-users',
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Пользователи"', 'links': links}
    return render(request, 'admin/list.html', context)

@login_required
def AddUserView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-user')

    form = AddUserForm()

    context = {'form': form, 'action': reverse('api-users'), 'search': True, 'link': 'list-user'}
    return render(request, 'admin/edit.html', context)

@login_required
def EditUserView(request, user_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-user')

    user = GetUser(user_id, True)
    groups = GroupsListUserAPIView().get(request = request, user_id = user_id).data
    form = EditUserForm(instance = user)

    context = {'form': form, 'groups': groups, 'search': True, 'link': 'list-user', 'delete_link': 'delete-user'}
    return render(request, 'admin/edit_user.html', context)

@login_required
def DeleteUserView(request, user_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-user')

    item = GetUser(user_id)
    form = DeleteUserForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-user', kwargs = {'user_id': user_id}), 'link': 'list-user'}
    return render(request, 'admin/delete.html', context)

@login_required
def GroupsListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-groups')

    items = GroupsListAPIView().get(request = request).data
    cols = ['Наименование']
    links = {
        'add_link': 'add-group',
        'edit_link': 'edit-group',
        'delete_link': 'api-delete-groups',
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Группы"', 'links': links}
    return render(request, 'admin/list.html', context)

@login_required
def AddGroupView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-groups')

    permissions = PermissionsListAPIView().get(request = request).data
    form = UserGroupForm()

    context = {'form': form, 'permissions': permissions, 'action': reverse('api-groups'), 'link': 'list-groups'}
    return render(request, 'admin/edit_group.html', context)

@login_required
def EditGroupView(request, group_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-groups')

    group = GetGroup(group_id)
    permissions = PermissionsListGroupAPIView().get(request = request, group_id = group_id).data
    form = UserGroupForm(instance = group)

    context = {'form': form, 'permissions': permissions, 'method': 'PUT', 'action': reverse('api-edit-group', kwargs = {'group_id': group_id}), 'link': 'list-groups', 'delete_link': 'delete-group'}
    return render(request, 'admin/edit_group.html', context)

@login_required
def DeleteGroupView(request, group_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-groups')

    group = GetGroup(group_id)
    form = DeleteUserGroupForm(instance = group)

    context = {'form': form, 'action': reverse('api-edit-group', kwargs = {'group_id': group_id}), 'link': 'list-groups'}
    return render(request, 'admin/delete.html', context)

@login_required
def OrganizationListView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-organization')

    items = OrganizationsListAPIView().get(request = request).data
    cols = ['Наименование']
    links = {
        'add_link': 'add-organization',
        'edit_link': 'edit-organization',
        'delete_link': 'api-delete-organizations',
    }

    context = {'items': items, 'cols': cols, 'label': 'Справочник "Организации"', 'links': links}
    return render(request, 'admin/list.html', context)

@login_required
def AddOrganizationView(request):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-organization')

    form = OrganizationForm()
    formsets = [
        {'key': 'contacts', 'formset': [ContactForm()], 'label': 'Контактное лицо'},
    ]

    context = {'form': form, 'formsets': formsets, 'action': reverse('api-organizations'), 'link': 'list-organization'}
    return render(request, 'admin/api_edit_formset.html', context)

@login_required
def EditOrganizationView(request, organization_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-organization')

    item = GetOrganization(organization_id, relates = True)
    form = OrganizationForm(instance = item)
    contacts = [ContactForm()]
    for contact in item.contacts.all():
        contacts.append(ContactForm(instance = contact))
    formsets = [
        {'key': 'contacts', 'formset': contacts, 'label': 'Контактное лицо'},
    ]

    context = {'form': form, 'formsets': formsets, 'method': 'PUT', 'action': reverse('api-edit-organizations', kwargs = {'organization_id': organization_id}), 'link': 'list-organization', 'delete_link': 'delete-organization'}
    return render(request, 'admin/api_edit_formset.html', context)

@login_required
def DeleteOrganizationView(request, organization_id):
    if not request.user.groups.filter(name = 'Администратор').exists():
        return redirect('login', link = 'list-organization')

    item = GetOrganization(organization_id)
    form = OrganizationDeleteForm(instance = item)

    context = {'form': form, 'action': reverse('api-edit-organizations', kwargs = {'organization_id': organization_id}), 'link': 'list-organization'}
    return render(request, 'admin/delete.html', context)

@login_required
def ContactsListView(request):
    contacts = ContactsListAPIView().get(request, organization_id = request.user.organization_id).data

    context = {'contacts': contacts}
    return render(request, 'accounts/contacts.html', context)

@login_required
def AddContactView(request):
    form = OrganizationContactForm()

    context = {'form': form, 'action': reverse('api-contacts')}
    return render(request, 'accounts/edit.html', context)

@login_required
def EditContactView(request, contact_id):
    contact = GetContact(contact_id)

    if not request.user.organization_id == contact.organization_id:
        return redirect('login')
    form = OrganizationContactForm(instance = contact)

    context = {'form': form, 'method': 'PUT', 'action': reverse('api-edit-contacts', kwargs = {'contact_id': contact_id})}
    return render(request, 'accounts/edit.html', context)
