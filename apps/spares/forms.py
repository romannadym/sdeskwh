from django import forms
from django.forms.models import inlineformset_factory
from django_select2 import forms as s2forms
from spares.models import PartNumberModel, SpareModel, SparePNModel

class PartNumberForm(forms.ModelForm):
    class Meta:
        model = PartNumberModel
        fields = '__all__'

class PartNumberDeleteForm(forms.ModelForm):
    class Meta:
        model = PartNumberModel
        fields = []

#ЗИП
class SpareForm(forms.ModelForm):
    class Meta:
        model = SpareModel
        exclude = ['barcode',]

class NumberWidget(s2forms.ModelSelect2Widget):
     search_fields = [
        'number__icontains',
    ]

class PNForm(forms.ModelForm):
    class Meta:
        model = SparePNModel
        fields = ['number',]
        widgets = {'number': NumberWidget}

SparePNFormset = inlineformset_factory(
    SpareModel, SparePNModel,
    form = PNForm,
    extra = 0
)

class SpareDeleteForm(forms.ModelForm):
    class Meta:
        model = SpareModel
        fields = []
