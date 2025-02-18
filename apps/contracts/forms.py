from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_select2 import forms as s2forms
from contracts.models import SupportLevelModel, ContractModel, ContractEquipmentModel

User = get_user_model()

class LevelForm(forms.ModelForm):
    class Meta:
        model = SupportLevelModel
        fields = '__all__'

class LevelDeleteForm(forms.ModelForm):
    class Meta:
        model = SupportLevelModel
        fields = []

class ClientWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'organization__name__icontains',
    ]
    def label_from_instance(self, obj):
        return str(obj.organization)

# class DateInput(forms.DateInput):
#     input_type = 'date'

class ContractForm(forms.ModelForm):
    # client = forms.ModelChoiceField(label = 'Заказчик', queryset = User.objects.filter(Q(is_active = True) & ~Q(email = 'serindework@mail.ru')))
    # end_user = forms.ModelChoiceField(label = 'Конечный пользователь', queryset = User.objects.filter(Q(is_active = True) & ~Q(email = 'serindework@mail.ru')))
    class Meta:
        model = ContractModel
        fields = '__all__'
        widgets = {
            'client': ClientWidget(attrs = {'data-minimum-input-length': 0}, queryset = User.objects.filter(Q(groups__name = 'Заказчик') & Q(is_active = True))),
            'end_user': ClientWidget(attrs = {'data-minimum-input-length': 0}, queryset = User.objects.filter(Q(groups__name = 'Заказчик') & Q(is_active = True))),
            # 'client': forms.Select(queryset = User.objects.filter(Q(is_active = True) & ~Q(email = 'serindework@mail.ru'))),
            'signed': forms.DateInput(attrs = {'class': 'date'}),
            'enddate': forms.DateInput(attrs = {'class': 'date'}),
        }

class ContractDeleteForm(forms.ModelForm):
    class Meta:
        model = ContractModel
        fields = []

class EquipmentWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'type__name__icontains',
        'brand__name__icontains',
        'model__name__icontains',
        'vendor__name__icontains',
    ]

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = ContractEquipmentModel
        exclude = ['contract',]
        widgets = {
            'equipment': EquipmentWidget,
            'sn': forms.TextInput(attrs = {'placeholder': 'Серийный номер'}),
            'support': forms.Select(attrs = {'placeholder': 'Тип поддержки'}),
        }

EquipmentFormset = inlineformset_factory(
    ContractModel, ContractEquipmentModel,
    fields = '__all__',
    form = EquipmentForm,
    extra = 0
)
