from rest_framework import serializers

from django.contrib.auth import get_user_model

from applications.models import AppPriorityModel, StatusModel, ApplicationModel, AppDocumentsModel, AppCommentModel, AppSpareModel

from accounts.api.serializers import ContactsListSerializer

from contracts.models import ContractModel, ContractEquipmentModel

from spares.api.serializers import SparesSerializer

class AppPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPriorityModel
        fields = '__all__'

class AppStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = '__all__'

class ContractsEquipmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label = 'Оборудование')
    class Meta:
        model = ContractEquipmentModel
        fields = ['name', 'sn']

class ContractSerializer(serializers.ModelSerializer):
    formatted_signed = serializers.CharField(label = 'Начало договора')
    formatted_enddate = serializers.CharField(label = 'Окончание договора')
    eqcontracts = ContractsEquipmentSerializer(many = True, read_only = True)

    class Meta:
        model = ContractModel
        fields = ['number', 'formatted_signed', 'formatted_enddate', 'eqcontracts']

class ClientSerializer(serializers.ModelSerializer):
    fio = serializers.CharField(label = 'ФИО')
    organization_name = serializers.CharField(label = 'Название органиации')
    contracts = ContractSerializer(many = True, read_only = True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'fio', 'inn', 'address', 'email', 'phone', 'organization_id', 'organization_name', 'contracts']

class AppDocumentsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label = 'Наименование файла', required = False)
    class Meta:
        model = AppDocumentsModel
        fields = ['document', 'name',]

class AddApplicationSerializer(serializers.ModelSerializer):
    documents = AppDocumentsSerializer(many = True, required = False)
    creator = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = ApplicationModel
        fields = ['priority', 'problem', 'contact', 'client', 'equipment', 'engineer', 'status', 'creator', 'documents']#

    def create(self, validated_data):
        documents = self.context['request'].data.getlist('documents')
        application = ApplicationModel.objects.create(**validated_data)

        if documents:
            documents_instance = [AppDocumentsModel(name = document.name, document = document, application = application) for document in documents]
            AppDocumentsModel.objects.bulk_create(documents_instance)

        return application

class ApplicationDetailsSerializer(serializers.ModelSerializer):
    formatted_date = serializers.CharField(label = 'Дата создания')
    status_name = serializers.CharField(label = 'Статус заявки')
    priority_name = serializers.CharField(label = 'Приоритет заявки')
    engineer_name = serializers.CharField(label = 'Инженер')
    contact_name = serializers.CharField(label = 'Контактное лицо')
    contact_email = serializers.CharField(label = 'Почта контактного лица')
    contact_phone = serializers.CharField(label = 'Телефон контактного лица')
    support_level = serializers.CharField(label = 'Тип поддержки')
    vendor_name = serializers.CharField(label = 'Вендор')
    equipment_name = serializers.CharField(label = 'Оборудование')
    documents = AppDocumentsSerializer(many = True, read_only = True)

    class Meta:
        model = ApplicationModel
        fields = [
            'id', 'formatted_date', 'status_id', 'status_name', 'priority_id', 'priority_name',
            'engineer_id', 'engineer_name', 'contact_id', 'contact_name', 'contact_email', 'contact_phone',
            'support_level', 'vendor_name', 'equipment_id', 'equipment_name', 'changed', 'problem', 'documents'
        ]

class AppCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppCommentModel
        fields = ['text', 'hide',]

    def update(self, instance, validated_data):
        instance.edited = True
        instance.text = validated_data.get('text', instance.text)
        instance.hide = validated_data.get('hide', instance.hide)
        instance.save()
        return instance

class AppSpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSpareModel
        fields = ['spare',]

class EditAppSpareSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationModel
        fields = ['appeqspare',]

class EditApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModel
        fields = ['engineer', 'priority', 'status', 'equipment']

class AddAppDocumentsSerializer(serializers.ModelSerializer):
    documents = AppDocumentsSerializer(many = True, required = False)
    class Meta:
        model = ApplicationModel
        fields = ['documents']

    def update(self, instance, validated_data):
        documents = self.context['request'].data.getlist('documents')

        if documents:
            documents_instance = [AppDocumentsModel(name = document.name, document = document, application = instance) for document in documents]
            AppDocumentsModel.objects.bulk_create(documents_instance)

        return instance

class ApplicationSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField(label = 'Идентификатор организации')
    formatted_date = serializers.CharField(label = 'Дата создания')
    status_name = serializers.CharField(label = 'Статус заявки')
    priority_name = serializers.CharField(label = 'Приоритет заявки')
    engineer_name = serializers.CharField(label = 'Инженер')
    contact_name = serializers.CharField(label = 'Контактное лицо')
    contact_email = serializers.CharField(label = 'Контактные данные (e-mail)')
    contact_phone = serializers.CharField(label = 'Контактные данные (телефон)')
    equipment_name = serializers.CharField(label = 'Оборудование')
    support_id = serializers.IntegerField(label = 'Идентификатор уровня поддержки')
    support_name = serializers.CharField(label = 'Уровень поддержки')
    vendor_name = serializers.CharField(label = 'Вендор')
    documents = AppDocumentsSerializer(many = True, required = False)

    class Meta:
        model = ApplicationModel
        fields = [
            'id', 'formatted_date', 'organization_id', 'status_id', 'status_name', 'priority_id', 'priority_name',
            'engineer_id', 'engineer_name', 'contact_id', 'contact_name', 'contact_email', 'contact_phone',
            'equipment_id', 'equipment_name', 'support_id', 'support_name', 'vendor_name', 'problem', 'documents',
        ]

#Для документации
class AppListSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(label = 'Наименование оборудования')
    status_name = serializers.CharField(label = 'Наименование статуса заявки')
    priority_name = serializers.CharField(label = 'Наименование приоритета заявки')
    organization_id = serializers.IntegerField(label = 'Идентификатор организации')
    organization_name = serializers.CharField(label = 'Наименование организации')
    end_user_organization_id = serializers.IntegerField(label = 'Идентификатор организации конечного пользователя')
    end_user_organization_name = serializers.CharField(label = 'Наименование организации конечного пользователя')
    engineer_last_name = serializers.CharField(label = 'Фамилия назначенного инженера')
    engineer_name = serializers.CharField(label = 'Полное имя назначенного инженера / e-mail')
    formatted_date = serializers.CharField(label = 'Дата создания')

    class Meta:
        model = ApplicationModel
        fields = [
            'id', 'equipment_id', 'equipment_name', 'status_id', 'status_name', 'problem', 'priority_id', 'priority_name',
            'organization_id', 'organization_name', 'end_user_organization_id', 'end_user_organization_name', 'engineer_id',
            'engineer_last_name', 'engineer_name', 'formatted_date'
        ]

class PermissionSerializer(serializers.Serializer):# Для документации
    is_admin = serializers.BooleanField(label = 'Администратор')
    is_engineer = serializers.BooleanField(label = 'Инженер')
    is_staff = serializers.BooleanField(label = 'Персонал')

class PaginationSerializer(serializers.Serializer):# Для документации
    page = serializers.IntegerField(label = 'Номер страницы')
    num_pages = serializers.IntegerField(label = 'Количество страниц')
    pages_range = serializers.ListField(child = serializers.IntegerField(), label = 'Диапазон страниц')
    has_next = serializers.BooleanField(label = 'Есть следующая страница')
    has_previous = serializers.BooleanField(label = 'Есть предыдущая страница')

class EngineerListSerializer(serializers.ModelSerializer):# Для документации
    name = serializers.CharField(label = 'Имя инженера')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

class ListSerializer(serializers.Serializer):# Для документации
    applications = AppListSerializer(many = True)
    statuses = AppStatusSerializer(many = True)
    permissions = PermissionSerializer()
    application_link = serializers.CharField(label = 'Тип ссылки')
    pagination = PaginationSerializer()
    priorities = AppPrioritySerializer(many = True)
    engineers = EngineerListSerializer(many = True)
    client = ClientSerializer()

class OrganizationEquipmentSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(label = 'Наименование оборудования')
    class Meta:
        model = ContractEquipmentModel
        fields = ['id', 'equipment_id', 'equipment_name']

class ContactsEquipmentSerializer(serializers.Serializer):# Для документации
    contacts = ContactsListSerializer(many = True)
    equipments = OrganizationEquipmentSerializer(many = True)

class ClientsAppFormSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(label = 'Наименование организации')
    name = serializers.CharField(label = 'ФИО заказчика / e-mail')
    class Meta:
        model = get_user_model()
        fields = ['id', 'organization_name', 'name']

class AppFormSerializer(serializers.Serializer):# Для документации
    priorities = AppPrioritySerializer(many = True)
    permissions = PermissionSerializer()
    clients = ClientsAppFormSerializer(many = True)

class HistorySerializer(serializers.Serializer):# Для документации
    id = serializers.IntegerField(label = 'Идентификатор')
    pubdate = serializers.CharField(label = 'Дата создания')
    text = serializers.CharField(label = 'Текст')
    hide = serializers.BooleanField(label = 'Скрыть от клиента')
    author_name = serializers.CharField(label = 'Автор')
    formatted_date = serializers.CharField(label = 'Форматированная дата создания')
    record_type = serializers.CharField(label = 'Тип записи')

class EditAppFormSerializer(serializers.Serializer):# Для документации
    application = ApplicationDetailsSerializer()
    history = HistorySerializer(many = True)
    spares = SparesSerializer(many = True)
    permissions = PermissionSerializer()

class CommentsSerializer(serializers.ModelSerializer):# Для документации
    formatted_date = serializers.CharField(label = 'Дата создания')
    author_name = serializers.CharField(label = 'ФИО автора')
    class Meta:
        model = AppCommentModel
        fields = ['id', 'text', 'formatted_date', 'author_name']

class CommentsListSerializer(serializers.Serializer):# Для документации
    comments = CommentsSerializer(many = True)

class HistoryInfoSerializer(serializers.Serializer):# Для документации
    id = serializers.IntegerField(label = 'Идентификатор')
    text = serializers.CharField(label = 'Текст')
    author_name = serializers.CharField(label = 'Автор')
    formatted_date = serializers.CharField(label = 'Форматированная дата создания')

class ApplicationInfoSerializer(serializers.Serializer):# Для документации:
    application = ApplicationSerializer()
    history = HistoryInfoSerializer(many = True)
    permissions = PermissionSerializer()
