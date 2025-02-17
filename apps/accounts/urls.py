from django.urls import path
from accounts.views import UserListView, AddUserView, EditUserView, DeleteUserView
from accounts.views import GroupsListView, AddGroupView, EditGroupView, DeleteGroupView
from accounts.views import OrganizationListView, AddOrganizationView, EditOrganizationView, DeleteOrganizationView
from accounts.views import ContactsListView, AddContactView, EditContactView

from accounts.api.api import ContactsListAPIView, ContactAPIView
from accounts.api.api import OrganizationsListAPIView, EditOrganizationAPIView, OrganizationsDeleteAPIView
from accounts.api.api import UsersListAPIView, EditUserAPIView, UsersDeleteAPIView
from accounts.api.api import GroupsListAPIView, PermissionsListGroupAPIView, GroupsListUserAPIView, EditGroupAPIView, GroupsDeleteAPIView
from accounts.api.api import PermissionsListAPIView

urlpatterns = [
    path('users/', UserListView, name = 'list-user'),
    path('users/add/', AddUserView, name = 'add-user'),
    path('users/edit/<int:user_id>', EditUserView, name = 'edit-user'),
    path('users/delete/<int:user_id>', DeleteUserView, name = 'delete-user'),

    path('groups/', GroupsListView, name = 'list-groups'),
    path('groups/add/', AddGroupView, name = 'add-group'),
    path('groups/edit/<int:group_id>', EditGroupView, name = 'edit-group'),
    path('groups/delete/<int:group_id>', DeleteGroupView, name = 'delete-group'),

    path('organizations/', OrganizationListView, name = 'list-organization'),
    path('organizations/add/', AddOrganizationView, name = 'add-organization'),
    path('organizations/edit/<int:organization_id>', EditOrganizationView, name = 'edit-organization'),
    path('organizations/delete/<int:organization_id>', DeleteOrganizationView, name = 'delete-organization'),

    path('contacts/', ContactsListView, name = 'contacts-list'),
    path('contacts/add/', AddContactView, name = 'add-contact'),
    path('contacts/edit/<int:contact_id>', EditContactView, name = 'edit-contact'),

    path('api/contacts/<int:organization_id>', ContactsListAPIView.as_view(), name = 'api-contacts'),
    path('api/contacts/<int:contact_id>', ContactAPIView.as_view(), name = 'api-edit-contacts'),

    path('api/organizations/', OrganizationsListAPIView.as_view(), name = 'api-organizations'),
    path('api/organizations/edit/<int:organization_id>', EditOrganizationAPIView.as_view(), name = 'api-edit-organizations'),
    path('api/organizations/delete/', OrganizationsDeleteAPIView.as_view(), name = 'api-delete-organizations'),

    path('api/users/', UsersListAPIView.as_view(), name = 'api-users'),
    path('api/users/edit/<int:user_id>', EditUserAPIView.as_view(), name = 'api-edit-user'),
    path('api/users/delete/', UsersDeleteAPIView.as_view(), name = 'api-delete-users'),

    path('api/groups/', GroupsListAPIView.as_view(), name = 'api-groups'),
    path('api/groups/<int:user_id>', GroupsListUserAPIView.as_view(), name = 'api-user-groups'),
    path('api/groups/edit/<int:group_id>', EditGroupAPIView.as_view(), name = 'api-edit-group'),
    path('api/groups/delete/', GroupsDeleteAPIView.as_view(), name = 'api-delete-groups'),

    path('api/permissions/', PermissionsListAPIView.as_view(), name = 'api-permissions'),
    path('api/permissions/<int:group_id>', PermissionsListGroupAPIView.as_view(), name = 'api-group-permissions'),
]
