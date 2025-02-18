from django import forms
import floppyforms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.auth import get_user_model
from django.db.models import Q

from accounts.models import OrganizationContactModel
from contracts.models import ContractModel
from equipments.models import EquipmentModel, ModelModel
from spares.models import SpareModel, PartNumberModel, SparePNModel
from applications.models import ApplicationModel, AppDocumentsModel, AppStatusModel, StatusModel, AppCommentModel
from applications.models import AppSpareModel

class ClientChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.organization) + ' (' + str(obj) + ')'

class StaffApplicationForm(forms.ModelForm):
    client = ClientChoiceField(label = 'Заказчик', queryset = get_user_model().objects.filter(Q(groups__name = 'Заказчик') & Q(is_active = True) & ~Q(email = 'serindework@mail.ru')))
    contact = forms.ModelChoiceField(label = 'Контактное лицо', queryset = OrganizationContactModel.objects.none())

    class Meta:
        model = ApplicationModel
        fields = ['client', 'priority', 'equipment', 'problem', 'contact']

class ClientApplicationForm(forms.ModelForm):
    contact = forms.ModelChoiceField(label = 'Контактное лицо', queryset = OrganizationContactModel.objects.none())

    class Meta:
        model = ApplicationModel
        fields = ['priority', 'problem', 'equipment', 'contact',]

class ApplicationForm(forms.ModelForm):
    User = get_user_model()
    client = ClientChoiceField(label = 'Заказчик', queryset = User.objects.filter(Q(groups__name = 'Заказчик') & Q(is_active = True) & ~Q(email = 'serindework@mail.ru')))

    class Meta:
        model = ApplicationModel
        fields = ('priority', 'problem', 'contact', 'client', )
        widgets = {
            'problem': forms.Textarea(attrs = {'rows': '4'}),
        }

    def __init__(self, user = None, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        if user:
            from applications.models import AppPriorityModel
            priority = AppPriorityModel.objects.get(id = 3)

            self.fields['client'].initial = user
            self.fields['priority'].initial = priority
            self.fields['contact'].queryset = OrganizationContactModel.objects.filter(Q(organization = user.organization) & ~Q(email = 'serindework@mail.ru'))

AppDocumentsFormset = inlineformset_factory(
    ApplicationModel, AppDocumentsModel,
    fields = ('document', 'application'),
    extra = 1
)

EditAppDocumentsFormset = inlineformset_factory(
    ApplicationModel, AppDocumentsModel,
    fields = ('name', 'document', 'application'),
    extra = 0
)

class AppStatusForm(forms.ModelForm):
    class Meta:
        model = AppStatusModel
        fields = ('status', )

    def __init__(self, st = None, *args, **kwargs):
        super(AppStatusForm, self).__init__(*args, **kwargs)

        from django.db.models import Q
        self.fields['status'].queryset = StatusModel.objects.filter(~Q(id = 6) & ~Q(id = 1))

        if self.data:
            self.fields['status'].queryset = StatusModel.objects.all()

AppStatusFormset = inlineformset_factory(
    ApplicationModel, AppStatusModel,
    form = AppStatusForm,
    fields = ('status', ),
    extra = 0,
    max_num = 1
)

class AppEditCommentForm(forms.ModelForm):
    class Meta:
        model = AppCommentModel
        fields = ('text', 'hide')
        # widgets = {
        #     'text': forms.Textarea(attrs = {'maxlength': '1000'}),
        # }

    def clean_text(self):
        from string import printable

        cyrillic_letters = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        allowed_chars = cyrillic_letters + printable

        s = self.cleaned_data.get('text', '').strip()
        result = ''.join([c for c in s if c in allowed_chars])
        return result

class AppCommentForm(forms.ModelForm):
    class Meta:
        model = AppCommentModel
        fields = ('text', )
        # widgets = {
        #     'text': forms.Textarea(attrs = {'maxlength': '1000'}),
        # }

    def clean_text(self):
        from string import printable

        cyrillic_letters = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        allowed_chars = cyrillic_letters + printable

        s = self.cleaned_data.get('text', '').strip()
        result = ''.join([c for c in s if c in allowed_chars])
        return result

class AppDeleteCommentForm(forms.ModelForm):
    class Meta:
        model = AppCommentModel
        fields = []

class AppApproveForm(forms.ModelForm):
    class Meta:
        model = AppStatusModel
        fields = ('status', )

AppApproveFormset = inlineformset_factory(
    ApplicationModel, AppStatusModel,
    form = AppApproveForm,
    fields = ('status', ),
    extra = 0,
    max_num = 1
)

class EditApplicationForm(forms.ModelForm):
    class Meta:
        model = ApplicationModel
        fields = ('priority', 'engineer',)

    def __init__(self, *args, **kwargs):
        super(EditApplicationForm, self).__init__(*args, **kwargs)

        User = get_user_model()
        self.fields['engineer'].queryset = User.objects.filter(groups__name = 'Инженер')
        # for s in self.status:
        #     s.status.queryset = StatusModel.objects.filter(id=1)
        #     # self.status.forms['status'] = AppStatusFormset(queryset = StatusModel.objects.filter(id=1))

class EquipmentForm(forms.ModelForm):

    class Meta:
        model = EquipmentModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)

        # self.fields['model'].queryset = ModelModel.objects.none()
        #
        # if self.data.get(self.add_prefix('brand')):
        #     brand = self.data.get(self.add_prefix('brand'))
        #     # self.fields['model'].queryset = ModelModel.objects.filter(brand_id = int(brand))
        # elif self.instance.pk:
        #     self.fields['model'].queryset = ModelModel.objects.filter(brand = self.instance.brand)

# class ContractForm(forms.ModelForm):
#     class Meta:
#         model = ContractModel
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(ContractForm, self).__init__(*args, **kwargs)
#
#         if not self.instance.pk:
#             User = get_user_model()
#             self.fields['client'].queryset = User.objects.filter(Q(groups__name = 'Заказчик') & Q(is_active = True) & ~Q(email = 'serindework@mail.ru'))

# class Input(floppyforms.CharField):
#     type = 'datalist'
#     datalist = []

class SparePNAdminForm(forms.ModelForm):
    number = floppyforms.CharField(label = 'Партномер', widget = floppyforms.widgets.Input(datalist = [''], attrs = {'autocomplete': 'off'}))

    class Meta:
        model = SparePNModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SparePNAdminForm, self).__init__(*args, **kwargs)

        if self.obj:
            self.fields['number'].widget.datalist = PartNumberModel.objects.values_list('number', flat = True)
        if self.instance.pk:
            self.initial['number'] = str(self.instance)

    def clean(self):
        super().clean()

        number = self.cleaned_data.get('number')
        pn = PartNumberModel.objects.get(number = number)
        if pn:
            self.cleaned_data['number'] = pn

class SpareAdminForm(forms.ModelForm):
    class Meta:
        model = SpareModel
        fields = '__all__'
        exclude = ['barcode', ]

class SpareForm(forms.ModelForm):
    class Meta:
        model = AppSpareModel
        # fields = ('spare', )
        exclude = ['author', 'pubdate',]

    def __init__(self, *args, **kwargs):
        super(SpareForm, self).__init__(*args, **kwargs)

        self.fields['spare'].required = False

        self.fields['spare'].queryset = SpareModel.objects.all()
        # spare = self.data.get('spare')
        # self.fields['spare'].queryset = SpareModel.objects.filter(Q(model__name__icontains = spare) | Q())

AppSpareFormset = inlineformset_factory(
    ApplicationModel, AppSpareModel,
    form = SpareForm,
    extra = 0
)

class SpareLoadForm(forms.Form):
    excel = forms.FileField(label = 'Файл')
