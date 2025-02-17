from django import forms

class ImportForm(forms.Form):
    excel = forms.FileField(label = 'Файл')
