from django import forms

class GetInTouchForm(forms.Form):
    name = forms.CharField(max_length = 250, label = "Ваше имя", widget = forms.TextInput(attrs = {'placeholder': 'Ваше имя'}))
    email = forms.EmailField(max_length = 50, label = "Ваш E-mail", widget = forms.EmailInput(attrs = {'placeholder': 'Ваш E-mail'}))
    text = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Комментарии', 'rows': 2}), label = "Комментарии")
