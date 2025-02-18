from django import forms
from django_select2 import forms as s2forms
from equipments.models import TypeModel, VendorModel, BrandModel, ModelModel, EquipmentModel

class TypeForm(forms.ModelForm):
    class Meta:
        model = TypeModel
        fields = '__all__'

class TypeDeleteForm(forms.ModelForm):
    class Meta:
        model = TypeModel
        fields = []

class VendorForm(forms.ModelForm):
    class Meta:
        model = VendorModel
        fields = '__all__'

class VendorDeleteForm(forms.ModelForm):
    class Meta:
        model = VendorModel
        fields = []

class BrandForm(forms.ModelForm):
    class Meta:
        model = BrandModel
        fields = '__all__'

class BrandDeleteForm(forms.ModelForm):
    class Meta:
        model = BrandModel
        fields = []

class ModelForm(forms.ModelForm):
    class Meta:
        model = ModelModel
        fields = '__all__'

class ModelDeleteForm(forms.ModelForm):
    class Meta:
        model = ModelModel
        fields = []

class NameWidget(s2forms.ModelSelect2Widget):
     search_fields = [
        'name__icontains',
    ]

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = '__all__'
        widgets = {
            'type': NameWidget(attrs = {'data-minimum-input-length': 0}),
            'brand': NameWidget(attrs = {'data-minimum-input-length': 0}),
            'model': NameWidget(dependent_fields = {'brand': 'brand'}, attrs = {'data-minimum-input-length': 0}),
            'vendor': NameWidget(attrs = {'data-minimum-input-length': 0}),
        }

class EquipmentDeleteForm(forms.ModelForm):
    class Meta:
        model = EquipmentModel
        fields = []
