from rest_framework.permissions import BasePermission

class IsAppAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name = 'Администратор').exists():
           return True
        return False

class IsAppStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name = 'Администратор').exists() or request.user.groups.filter(name = 'Инженер').exists():
           return True
        return False
