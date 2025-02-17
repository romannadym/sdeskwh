from django.db.models import Q, F, Value, Case, When

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import APIException

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from accounts.models import User, OrganizationModel, OrganizationContactModel

from integrator.apps.parsers import NestedMultipartParser

from accounts.api.serializers import *

from integrator.apps.functions import is_admin_or_engineer

@extend_schema(tags = ['Контакты организации (Done)'])
class ContactsListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        summary = 'Список контактов организации',
        description = '<ol><li>"id" - Идентификатор контакта</li><li>"fio" - ФИО контакта</li></ol>',
        parameters = [
            OpenApiParameter(name = 'organization_id', description = 'Идентификатор организации', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = ContactsListSerializer(many = True))}
    )
    def get(self, request, organization_id, *args, **kwargs):
        contacts = OrganizationContactModel.objects.filter(Q(organization_id = organization_id) & ~Q(email = 'serindework@mail.ru'))
        serializer = ContactsListSerializer(contacts, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Добавление контакта',
        description = '<ol><li>"fio" - ФИО</li><li>"email" - Адрес электронной почты</li><li>"phone" - Телефон</li></ol>',
        request = ContactSerializer(),
        parameters = [
            OpenApiParameter(name = 'organization_id', description = 'Идентификатор организации', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(201, 'application/json'): OpenApiResponse(response = ContactSerializer())}
    )
    def post(self, request, organization_id, *args, **kwargs):
        if is_admin_or_engineer(request.user):
            return Response({'error': 'Функционал доступен только для клиентов'}, status = status.HTTP_403_FORBIDDEN)

        serializer = ContactSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(organization_id = organization_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags = ['Контакты организации (Done)'])
class ContactAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        summary = 'Изменение контакта',
        description = '<ol><li>"fio" - ФИО</li><li>"email" - Адрес электронной почты</li><li>"phone" - Телефон</li></ol>',
        request = ContactSerializer(),
        parameters = [
            OpenApiParameter(name = 'contact_id', description = 'Идентификатор контакта', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = ContactSerializer())}
    )
    def put(self, request, contact_id, *args, **kwargs):
        contact = GetContact(contact_id)
        if not request.user.organization_id == contact.organization_id:
            return Response({'error': 'Доступ запрещен'}, status = status.HTTP_403_FORBIDDEN)

        serializer = ContactSerializer(contact, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление контакта',
        parameters = [
            OpenApiParameter(name = 'contact_id', description = 'Идентификатор контакта', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Объект удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Объект удален'})])}
    )
    def delete(self, request, contact_id, *args, **kwargs):
        contact = GetContact(contact_id)

        if not request.user.organization_id == contact.organization_id:
            return Response({'error': 'Доступ запрещен'}, status = status.HTTP_403_FORBIDDEN)

        contact.delete()
        return Response({'message': 'Объект удален'}, status = status.HTTP_200_OK)

def GetContact(contact_id):
    try:
        return OrganizationContactModel.objects.get(id = contact_id)
    except:
        raise APIException('Контакт с id = ' + str(contact_id) + ' не найден')

#Список организаций
@extend_schema(
    tags = ['Организации (Done)'],
)
class OrganizationsListAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        summary = 'Список организаций',
        description = '<ol><li>"id" - Идентификатор организации</li><li>"name" - Наименование организации</li></ol>',
        responses = {(200, 'application/json'): OpenApiResponse(response = OrganizationsSerializer(many = True))}
    )
    def get(self, request, *args, **kwargs):

        list = OrganizationModel.objects.all()
        serializer = OrganizationsSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        request = EditOrganizationSerializer(),
        summary = 'Добавление организации',
        description = '<ol><li>"name" - Наименование организации</li><li>"contacts" - список контактов, где\
        <ul><li>"fio" - ФИО контакта</li><li>"email" - Адрес электронной почты контакта</li><li>"phone" - Телефон контакта.</li></ul>\
        </li></ol><b>"id", "DELETE" используются в методе PUT, в этом указывать их ненужно</b>',
        responses = {(201, 'application/json'): OpenApiResponse(response = EditOrganizationSerializer())}
    )
    def post(self, request, *args, **kwargs):
        serializer = EditOrganizationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Элемент создан'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags = ['Организации (Done)'],
)
class EditOrganizationAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        request = EditOrganizationSerializer(),
        summary = 'Изменение организации',
        description = '<ol><li>"name" - Наименование организации</li><li>"contacts" - список контактов, где\
        <ul><li>"id" - Идентификатор контакта</li><li>"fio" - ФИО контакта</li><li>"email" - Адрес электронной почты контакта</li><li>"phone" - Телефон контакта.</li><li>"DELETE" - Отметка об удалении ("True" - контакт будет удален)</li></ul>\
        </li></ol>',
        parameters = [
            OpenApiParameter(name = 'organization_id', description = 'Идентификатор организации', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = EditOrganizationSerializer())}
    )
    def put(self, request, organization_id, *args, **kwargs):
        organization = GetOrganization(organization_id)

        serializer = EditOrganizationSerializer(organization, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление организации',
        parameters = [
            OpenApiParameter(name = 'organization_id', description = 'Идентификатор организации', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Объект удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Объект удален'})])}
    )
    def delete(self, request, organization_id, *args, **kwargs):
        organization = GetOrganization(organization_id)
        organization.delete()
        return Response({'message': 'Объект удален'}, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Организации (Done)'],
)
class OrganizationsDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Удаление нескольких организаций',
        description = '"id" - список идентификаторов организаций',
        request = OrganizationsDeleteSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элементы удалены'}, examples = [OpenApiExample('Пример', value = {'message': 'Элементы удалены'})])}
    )
    def post(self, request, *args, **kwargs):
        serializer = OrganizationsDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            OrganizationModel.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status = status.HTTP_400_BAD_REQUEST)

def GetOrganization(organization_id, relates = False):
    try:
        if relates:
            return OrganizationModel.objects.prefetch_related('contacts').get(id = organization_id)
        else:
            return OrganizationModel.objects.get(id = organization_id)
    except:
        raise APIException('Организация с id = ' + str(organization_id) + ' не найдена')

#Список пользователей
@extend_schema(
    tags = ['Пользователи (Done)'],
)
class UsersListAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Список пользователей',
        description = '<ol><li>"id" - Идентификатор пользователя</li><li>"email" - Адрес электронной почты пользователя</li>\
            <li>"organization_name" - Наименование организации пользователя</li><li>"phone" - Телефон пользователя</li><li>"img" - Адрес картинки роли</li>\
            <li>"groups" - Список наименований групп</li></ol>',
        responses = {(200, 'application/json'): OpenApiResponse(response = UsersSerializer(many = True))}
    )
    def get(self, request, *args, **kwargs):
        list = User.objects.filter(~Q(email = 'serindework@mail.ru')).annotate(
            organization_name = F('organization__name')
        )

        serializer = UsersSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Добавление пользователя',
        description = '<b>Внимание!!!</b> В примере указано поле <b>"password"</b> сериализатора, но сам метод требует <b>вместо этого поля</b> указывать <b>"password1" и "password2"</b>\
            <ol><li>"email" - Адрес электронной почты пользователя</li><li><b>"password1" - Пароль</b></li><li><b>"password2" - Подтверждение пароля</b></li>\
            <li>"first_name" - Имя пользователя</li><li>"last_name" - Фамилия пользователя</li><li>"inn" - ИНН пользователя</li>\
            <li>"organization" - Идентификатор организации пользователя</li><li>"address" - Адрес пользователя</li><li>"phone" - Телефон пользователя</li><li>"telegram" - Идентификатор пользователя в телеграме</li></ol>',
        request = AddUserSerializer(),
        responses = {(201, 'application/json'): OpenApiResponse(response = AddUserSerializer())}
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' not in request.data.keys():
            if data['password1'] != data['password2']:
                return Response({'error': 'Пароли не совпадают'}, status = status.HTTP_406_NOT_ACCEPTABLE)

            data['password'] = data['password1']

        serializer = AddUserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags = ['Пользователи (Done)'],
)
class EditUserAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        request = EditUserSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = EditUserSerializer())},
        summary = 'Изменение пользователя',
        description = '<ol><li>"email" - Адрес электронной почты пользователя</li><li>"organization" - Идентификатор организации пользователя</li>\
            <li>"first_name" - Имя пользователя</li><li>"last_name" - Фамилия пользователя</li><li>"is_superuser" - Статус суперпользователя</li>\
            <li>"is_staff" - Статус персонала</li><li>"is_active" - Активный</li><li>"inn" - ИНН пользователя</li>\
            <li>"address" - Адрес пользователя</li><li>"phone" - Телефон пользователя</li><li>"telegram" - Идентификатор пользователя в телеграме</li>\
            <li>"groups" - Список идентификаторов групп</li></ol>',
        parameters = [
            OpenApiParameter(name = 'user_id', description = 'Идентификатор пользователя', type = int, required = True, location = OpenApiParameter.PATH),
        ]
    )
    def put(self, request, user_id, *args, **kwargs):
        user = GetUser(user_id)
        serializer = EditUserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление пользователя',
        parameters = [
            OpenApiParameter(name = 'user_id', description = 'Идентификатор пользователя', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Объект удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Объект удален'})])}
    )
    def delete(self, request, user_id, *args, **kwargs):
        user = GetUser(user_id)
        user.delete()
        return Response({'message': 'Объект удален'}, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Пользователи (Done)'],
)
class UsersDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Удаление нескольких пользователей',
        description = '"id" - список идентификаторов пользователей',
        request = UsersDeleteSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элементы удалены'}, examples = [OpenApiExample('Пример', value = {'message': 'Элементы удалены'})])}
    )
    def post(self, request, *args, **kwargs):
        serializer = UsersDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            User.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status=status.HTTP_400_BAD_REQUEST)

def GetUser(user_id, relates = False):
    try:
        if relates:
            return User.objects.prefetch_related('groups').get(id = user_id)
        else:
            return User.objects.get(id = user_id)
    except:
        raise APIException('Пользователь с id = ' + str(user_id) + ' не найден')

#Список групп
@extend_schema(
    tags = ['Группы пользователей (Done)'],
)
class GroupsListAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        summary = 'Список групп',
        description = '<ol><li>"id" - Идентификатор группы</li><li>"name" - Наименование группы</li></ol> Реквизит "contains" в этом методе не используется',
        responses = {(200, 'application/json'): OpenApiResponse(response = GroupsSerializer(many = True))},
    )
    def get(self, request, *args, **kwargs):
        list = Group.objects.all()

        serializer = GroupsSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Добавление группы',
        description = '<ol><li>"name" - Наименование группы</li><li>"permissions" - Список идентификаторов разрешений</li></ol>',
        request = EditGroupSerializer(),
        responses = {(201, 'application/json'): OpenApiResponse(response = EditGroupSerializer())},
    )
    def post(self, request, *args, **kwargs):
        serializer = EditGroupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags = ['Группы пользователей (Done)'],
)
class GroupsListUserAPIView(APIView):
    @extend_schema(
        summary = 'Список групп с принадлежностью конкретному пользователю',
        description = '<ol><li>"id" - Идентификатор группы</li><li>"name" - Наименование группы</li><li>"contains" - Признак наличия пользователя в группе</li></ol>',
        parameters = [
            OpenApiParameter(name = 'user_id', description = 'Идентификатор пользователя', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = GroupsSerializer(many = True))},
    )
    def get(self, request, user_id, *args, **kwargs):
        list = Group.objects.all().annotate(
            contains = Value(False)
        )
        user = GetUser(user_id, True)
        if user:
            user_groups_ids = user.groups.all().values_list('id', flat = True)
            for group in list:
                if group.id in user_groups_ids:
                    group.contains = True

        serializer = GroupsSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Группы пользователей (Done)'],
)
class EditGroupAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        request = EditGroupSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = EditGroupSerializer())},
        summary = 'Изменение группы',
        description = '<ol><li>"name" - Наименование группы</li><li>"permissions" - Список идентификаторов разрешений</li></ol>',
        parameters = [
            OpenApiParameter(name = 'group_id', description = 'Идентификатор группы', type = int, required = True, location = OpenApiParameter.PATH),
        ]
    )
    def put(self, request, group_id, *args, **kwargs):
        group = GetGroup(group_id)
        serializer = EditGroupSerializer(group, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление группы',
        parameters = [
            OpenApiParameter(name = 'group_id', description = 'Идентификатор группы', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Объект удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Объект удален'})])}
    )
    def delete(self, request, group_id, *args, **kwargs):
        group = GetGroup(group_id)
        group.delete()
        return Response({'message': 'Объект удален'}, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Группы пользователей (Done)'],
)
class GroupsDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Удаление нескольких групп',
        description = '"id" - список идентификаторов групп',
        request = GroupsDeleteSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элементы удалены'}, examples = [OpenApiExample('Пример', value = {'message': 'Элементы удалены'})])}
    )
    def post(self, request, *args, **kwargs):
        serializer = GroupsDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            Group.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status=status.HTTP_400_BAD_REQUEST)

def GetGroup(group_id, relates = False):
    try:
        if relates:
            return Group.objects.prefetch_related('permissions').get(id = group_id)
        else:
            return Group.objects.get(id = group_id)
    except:
        raise APIException('Группа с id = ' + str(group_id) + ' не найдена')

#Список разрешений
@extend_schema(
    tags = ['Разрешения (Done)'],
)
class PermissionsListAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Список разрешений',
        description = '<ol><li>"id" - Идентификатор разрешения</li><li>"name" - Наименование разрешения</li><li>"application" - Наименование приложения разрешения</li></ol> Реквизит "contains" в этом методе не используется',
        responses = {(200, 'application/json'): OpenApiResponse(response = PermissionsSerializer(many = True))},
    )
    def get(self, request, *args, **kwargs):
        list = Permission.objects.all().annotate(application = F('content_type__app_label'))

        serializer = PermissionsSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Разрешения (Done)'],
)
class PermissionsListGroupAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Список разрешений с принадлежностью группе',
        description = '<ol><li>"id" - Идентификатор разрешения</li><li>"name" - Наименование разрешения</li>\
        <li>"application" - Наименование приложения разрешения</li><li>"contains" - Признак наличия разрешения в группе</li></ol>',
        parameters = [
            OpenApiParameter(name = 'group_id', description = 'Идентификатор группы', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = PermissionsSerializer(many = True))},
    )
    def get(self, request, group_id, *args, **kwargs):
        list = Permission.objects.all().annotate(
            application = F('content_type__app_label'),
            contains = Value(False)
        )

        group = GetGroup(group_id, True)
        if group:
            group_permissions = group.permissions.values_list('id', flat = True)
            for permission in list:
                if permission.id in group_permissions:
                    permission.contains = True

        serializer = PermissionsSerializer(list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
