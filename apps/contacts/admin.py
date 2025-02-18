from django.contrib import admin

from contacts.models import ContactModel

class ContactAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request, obj = None):
        return False

    def has_delete_permission(self, request, obj = None):
        return False

admin.site.register(ContactModel, ContactAdminModel)
