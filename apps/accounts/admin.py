from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from django.utils.html import format_html

from accounts.models import User, OrganizationModel, OrganizationContactModel

@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'inn', 'organization', 'address', 'phone', 'telegram')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'inn', 'organization', 'address', 'phone', 'telegram'),
        }),
    )
    list_display = ('email', 'icons', 'first_name', 'last_name', 'is_staff', 'organization', 'roles')
    search_fields = ('email', 'first_name', 'last_name', 'organization')
    ordering = ('email',)

    def roles(self, obj):
        return u" %s" % (u", ".join([record.name for record in obj.groups.all()]))
    roles.short_description = 'Роли'

    def icons(self, obj):
        img = static('img/icons/client.png')
        if obj.groups.filter(name = 'Администратор').exists():
            img = static('img/icons/admin.png')
        elif obj.groups.filter(name = 'Инженер').exists():
            img = static('img/icons/engineer.png')
        return format_html('<img src="{}" style="height:16px;">', img)
    icons.short_description = ''

class ContactModelInline(admin.StackedInline):
    model = OrganizationContactModel

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Информация для связи'

class OrganizationModelAdmin(admin.ModelAdmin):
    inlines = [ContactModelInline, ]


admin.site.register(OrganizationModel, OrganizationModelAdmin)
