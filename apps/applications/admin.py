from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from nested_admin import NestedModelAdmin, NestedStackedInline
from applications.models import AppPriorityModel, VendorModel, BrandModel, ModelModel, EquipmentModel, StatusModel, ContractModel, ContractEquipmentModel, ContractHistoryModel
from applications.models import SupportLevelModel, EquipmentTypeModel, ExecutorModel, EquipmentConfigModel, SparePartNumberModel
from applications.models import SpareModel, SparePNModel, ApplicationArchiveModel, AppSpareModel, InstalledBaseModel
from applications.forms import EquipmentForm, ContractForm, SpareAdminForm, SparePNAdminForm


class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'brand', 'type', 'model',)
    exclude = ('contract',)
    search_fields = ['brand__name', 'type__name', 'model__name', 'contract__number',]
    def contract_number(self, obj):
        return obj.contract.number
    contract_number.short_description = 'Номер договора'

class EquipmentModelInline(admin.StackedInline):
    model = ContractEquipmentModel
    form = EquipmentForm
    extra = 0

    verbose_name = "Оборудование"
    verbose_name_plural = "Оборудование"

    # def conf_inline(self, obj = None, *args, **kwargs):
    #     from django.template.loader import get_template
    #     context = getattr(self.modeladmin.response, 'context_data', None) or {}
    #     admin_view = EquipmentModelAdmin(self.model, self.modeladmin.admin_site).add_view(self.modeladmin.request)
    #     inline = admin_view.context_data['inline_admin_formsets']
    #     # d = context.copy()
    #     # d.update({'inline_admin_formset': inline})
    #     context['inline_admin_formset'] = inline[0]
    #     return get_template(inline.opts.template).render(context, self.modeladmin.request)

class ContractModelAdmin(admin.ModelAdmin):
    form = ContractForm
    # readonly_fields = ('organization')
    inlines = [EquipmentModelInline,]
    change_form_template = 'applications/my_change_form.html'
    change_list_template = 'applications/contracts_change_list.html'
    list_display = ('number', 'signed', 'enddate', 'client', 'organization')
    class Media:
        js = ('js/eq_models.js',)

    def organization(self, obj):
        if obj:
            if obj.client:
                return str(obj.client.organization)
            else:
                return 'Удалена учетная запись Ответственного лица'
        else:
            return ''
    organization.short_description = 'Организация'

    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ['number', 'signed', 'client', 'organization']
        else:
            return ['organization']

    def save_model(self, request, obj, form, change):
        if change:
            prev = ContractModel.objects.get(id = obj.pk)
        super().save_model(request, obj, form, change)
        if not change:
            ContractHistoryModel.objects.create(text = 'Договор создан', contract = obj, author = request.user)
        else:
            if 'enddate' in form.changed_data:
                ContractHistoryModel.objects.create(text = 'Дата окончания действия договора измененена c ' + prev.enddate.strftime('%d.%m.%Y') + ' на ' + form.cleaned_data['enddate'].strftime('%d.%m.%Y'), contract = obj, author = request.user)

    # def render_change_form(self, request, *args, **kwargs):
    #     self.request = request
    #     response = self.response = super().render_change_form(request, *args, **kwargs)
    #     return response
    #
    # def get_inline_instances(self, *args, **kwargs):
    #     yield from ((inline, vars(inline).update(modeladmin=self))[0] for inline in super().get_inline_instances(*args, **kwargs))

class ContractHistoryAdminModel(admin.ModelAdmin):
    list_display = ('text', 'contract', 'pubdate', 'author')
    def has_add_permission(self, request, obj = None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_delete_permission(self, request, obj = None):
        return False

class ApplicationArchiveAdminModel(admin.ModelAdmin):
    list_display = ('old_id', 'pubdate', 'client', 'equipment', 'problem')
    def has_add_permission(self, request, obj = None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_delete_permission(self, request, obj = None):
        return False

class SparePNModelInline(admin.StackedInline):
    model = SparePNModel
    form = SparePNAdminForm

    verbose_name = "Партномер"
    verbose_name_plural = "Партномера"

    def get_formset(self, request, obj=None, **kwargs):
        SparePNAdminForm.obj = obj
        return super(SparePNModelInline, self).get_formset(request, obj, **kwargs)

class SpareModelAdmin(admin.ModelAdmin):
    inlines = [SparePNModelInline, ]
    change_list_template = 'applications/spare_change_list.html'
    change_form_template = 'applications/spare_change_form.html'
    list_display = ('__str__', 'pns')#'quantity_colored',
    form = SpareAdminForm

    class Media:
        js = ('js/spare_admin.js',)

    def pns(self, obj):
        return u" %s" % (u", ".join([str(record.number) for record in SparePNModel.objects.filter(spare = obj)[:3]]))
    pns.short_description = 'Партномера'

    # def quantity_colored(self, obj):
    #     color = ''
    #     if obj.quantity < 2:
    #         color = 'red'
    #     return format_html('<b style="color:{};">{}</b>',color, obj.quantity)
    # quantity_colored.short_description = 'Количество'

class AppSpareModelHistory(admin.ModelAdmin):
    list_display = ('spare', 'application', 'equipment', 'client', 'pubdate', 'author')
    def has_add_permission(self, request, obj = None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_delete_permission(self, request, obj = None):
        return False

    def equipment(self, obj):
        return obj.application.equipment
    equipment.short_description = 'Оборудование'
    def client(self, obj):
        return str(obj.application.client) + ' (' + obj.application.client.organization + ')'
    client.short_description = 'Клиент'

    def get_list_display_links(self, request, list_display):
        self.list_display_links = (None, )
        return self.list_display_links

class InstalledBase(admin.ModelAdmin):
    list_display = ('client', 'equip', 'brand', 'type', 'model', 'sdate', 'edate',)
    list_display_links = None
    list_filter = ('brand', 'type', 'model')
    change_list_template = 'applications/installed_base_list.html'
    def has_add_permission(self, request, obj = None):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_delete_permission(self, request, obj = None):
        return False

    def client(self, obj):
        return str(obj.contract.client.organization)
    client.short_description = 'Заказчик'

    def equip(self, obj):
        return str(obj.model)
    equip.short_description = 'Оборудование'

    def sdate(self, obj):
        return obj.contract.signed.strftime('%d.%m.%Y')
    sdate.short_description = 'Старт поддержки'

    def edate(self, obj):
        return obj.contract.enddate.strftime('%d.%m.%Y')
    edate.short_description = 'Окончание поддержки'

admin.site.register(AppPriorityModel)
admin.site.register(VendorModel)
admin.site.register(BrandModel)
admin.site.register(ModelModel)
admin.site.register(ContractModel, ContractModelAdmin)
admin.site.register(EquipmentModel, EquipmentModelAdmin)
admin.site.register(InstalledBaseModel, InstalledBase)
admin.site.register(ContractHistoryModel, ContractHistoryAdminModel)
admin.site.register(StatusModel)
admin.site.register(SupportLevelModel)
admin.site.register(EquipmentTypeModel)
admin.site.register(SparePartNumberModel)
admin.site.register(SpareModel, SpareModelAdmin)
admin.site.register(ApplicationArchiveModel, ApplicationArchiveAdminModel)
admin.site.register(AppSpareModel, AppSpareModelHistory)
admin.site.register(ExecutorModel)
