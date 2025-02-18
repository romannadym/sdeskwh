from django import forms
from django_select2 import forms as s2forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
User = get_user_model()
from accounts.models import OrganizationModel, OrganizationContactModel
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple

class OrganizationWidget(s2forms.ModelSelect2Widget):
     search_fields = [
        'organization__icontains',
    ]

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'inn', 'organization', 'address', 'phone', 'telegram']
        widgets = {'organization': OrganizationWidget(attrs = {'data-minimum-input-length': 0})}

class EditUserForm(UserChangeForm):
    password = None
    groups = forms.ModelMultipleChoiceField(label = 'Группы', queryset = Group.objects.all(), help_text = 'Группы, к которым принадлежит данный пользователь. Пользователь получит все права, указанные в каждой из его/её групп.', required = True)
    class Meta:
        model = User
        exclude = ['last_login', 'date_joined', 'password', 'user_permissions']
        widgets = {'organization': OrganizationWidget(attrs = {'data-minimum-input-length': 0})}

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        if not self.data:
            user_groups = self.instance.groups.values_list('pk', flat = True)
            self.fields['groups'].queryset = Group.objects.filter(pk__in = user_groups)

class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

class UserGroupForm(forms.ModelForm):
    # permissions = forms.ModelMultipleChoiceField(label = 'Разрешения', queryset = Permission.objects.all(), help_text = 'Выбранные права', required = False)
    class Meta:
        model = Group
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(UserGroupForm, self).__init__(*args, **kwargs)
    #
    #     if not self.data and self.instance.pk:
    #         group_permissions = self.instance.permissions.values_list('pk', flat = True)
    #         self.fields['permissions'].queryset = Permission.objects.filter(pk__in = group_permissions)

class DeleteUserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = []

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = OrganizationModel
        fields = '__all__'

class OrganizationDeleteForm(forms.ModelForm):
    class Meta:
        model = OrganizationModel
        fields = []

class ContactForm(forms.ModelForm):
    class Meta:
        model = OrganizationContactModel
        fields = ['fio', 'email', 'phone']
        widgets = {
            'fio': forms.TextInput(attrs = {'placeholder': 'ФИО'}),
            'email': forms.TextInput(attrs = {'placeholder': 'Адрес электронной почты'}),
            'phone': forms.TextInput(attrs = {'placeholder': 'Телефон'})
        }

ContactFormset = inlineformset_factory(
    OrganizationModel, OrganizationContactModel,
    fields = '__all__',
    form = ContactForm,
    extra = 0
)

class OrganizationContactForm(forms.ModelForm):
    class Meta:
        model = OrganizationContactModel
        exclude = ['organization',]
