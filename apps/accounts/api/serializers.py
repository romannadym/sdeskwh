from rest_framework import serializers

from django.templatetags.static import static

from django.contrib.auth.models import Group, Permission

from accounts.models import User, OrganizationModel, OrganizationContactModel

class ContactsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationContactModel
        fields = ['id', 'fio']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationContactModel
        fields = ['fio', 'email', 'phone']

class EditContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label = 'Идентификатор', required = False)
    DELETE = serializers.BooleanField(label = 'Удалить', default = False, required = False)

    class Meta:
        model = OrganizationContactModel
        fields = ['id', 'fio', 'email', 'phone', 'DELETE']

#Список организаций
class OrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = '__all__'

class EditOrganizationSerializer(serializers.ModelSerializer):
    contacts = EditContactSerializer(many = True, required = False)

    class Meta:
        model = OrganizationModel
        fields = '__all__'

    def create(self, validated_data):
        contacts = validated_data.pop('contacts')
        organization = OrganizationModel.objects.create(**validated_data)

        if contacts:
            contacts_create = []
            for contact in contacts:
                if not contact['DELETE']:
                    contact.pop('DELETE')
                    contacts_create.append(
                        OrganizationContactModel(**contact, organization = organization)
                    )
            OrganizationContactModel.objects.bulk_create(contacts_create)
        return organization

    def update(self, instance, validated_data):
        fields = ['name',]

        for field in fields:
            setattr(instance, field, validated_data.get(field))
        instance.save()

        contacts = validated_data.pop('contacts')
        if contacts:
            contacts_create = []
            contacts_update = []
            contacts_delete = []
            for contact in contacts:
                if contact['DELETE'] and 'id' in contact.keys():
                    contacts_delete.append(contact['id'])
                elif not contact['DELETE']:
                    contact.pop('DELETE')

                    if 'id' in contact.keys():
                        contacts_update.append(OrganizationContactModel(**contact))
                    else:
                        contacts_create.append(OrganizationContactModel(**contact, organization = instance))

            if contacts_delete:
                OrganizationContactModel.objects.filter(id__in = contacts_delete, organization = instance).delete()
            if contacts_create:
                OrganizationContactModel.objects.bulk_create(contacts_create, ignore_conflicts = True)
            if contacts_update:
                OrganizationContactModel.objects.bulk_update(contacts_update, ['fio', 'email', 'phone'])

            return instance

class OrganizationsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = OrganizationModel
        fields = ['id']

#Список пользователей
class UsersSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(label = 'Наименование организации')
    img = serializers.SerializerMethodField(label = 'Изображение')
    groups = serializers.SlugRelatedField(many = True, read_only = True,  slug_field = 'name')

    class Meta:
        model = User
        fields = ['id', 'email', 'organization_name', 'phone', 'img', 'groups']

    def get_img(self, obj):
        user_groups = obj.groups.values_list('name', flat = True)
        if 'Администратор' in user_groups:
            return static('img/icons/admin.png')
        elif 'Инженер' in user_groups:
            return static('img/icons/engineer.png')
        elif 'Заказчик' in user_groups:
            return static('img/icons/client.png')
        return ''

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'inn', 'organization', 'address', 'phone', 'telegram']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        fields = ['first_name', 'last_name', 'inn', 'organization', 'address', 'phone', 'telegram']
        for field in fields:
            if not validated_data.get(field):
                validated_data.pop(field)

        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'organization', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'inn', 'address', 'phone', 'telegram', 'groups']
        extra_kwargs = {
            'is_superuser': {'default': False},
            'is_staff': {'default': False},
            'is_active': {'default': False},
            'last_name': {'default': ''},
            'first_name': {'default': ''},
        }

    def update(self, instance, validated_data):
        fields = ['email', 'organization', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'inn', 'address', 'phone', 'telegram']
        for field in fields:
            setattr(instance, field, validated_data.get(field))

        instance.save()

        groups = validated_data.pop('groups')
        if groups:
            user_groups = instance.groups.values_list('id', flat = True)
            groups_create = []
            groups_delete = []

            for group in user_groups:
                if group not in groups:
                    instance.groups.remove(group)

            for group in groups:
                if group not in user_groups:
                    instance.groups.add(group)

        return instance

class UsersDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = User
        fields = ['id',]

#Список групп
class GroupsSerializer(serializers.ModelSerializer):
    contains = serializers.BooleanField(label = 'Содержит пользователя', required = False)
    class Meta:
        model = Group
        fields = ['id', 'name', 'contains']

class EditGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'permissions',]

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)

        if permissions:
            group.permissions.set(permissions)

        return group

    def update(self, instance, validated_data):
        fields = ['name',]
        for field in fields:
            setattr(instance, field, validated_data.get(field))
        instance.save()

        permissions = validated_data.pop('permissions')
        if permissions:
            group_permissions = instance.permissions.values_list('id', flat = True)
            permissions_create = []
            permissions_delete = []

            for permission in group_permissions:
                if permission not in permissions:
                    instance.permissions.remove(permission)

            for permission in permissions:
                if permission not in group_permissions:
                    instance.permissions.add(permission)
        return instance

class GroupsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = Group
        fields = ['id',]

#Список разрешений
class PermissionsSerializer(serializers.ModelSerializer):
    application = serializers.CharField(label = 'Приложение')
    contains = serializers.BooleanField(label = 'Включено в группу', required = False)

    class Meta:
        model = Permission
        fields = ['id', 'name', 'application', 'contains']
