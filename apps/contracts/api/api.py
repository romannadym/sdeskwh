from django.db.models import F

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import APIException

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse

from integrator.apps.parsers import NestedMultipartParser

from contracts.api.serializers import *

from contracts.models import SupportLevelModel, ContractModel, ContractEquipmentModel

@extend_schema(
    tags = ['Уровни поддержки (Done)']
)
class SupportLevelsListAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Список уровней поддержки',
        description = '<ol><li>"id" - Идентификатор уровня поддержки</li>\
        <li>"priority" - Приоритет отображения уровня (упорядочивание от меньшего к большему)</li>\
        <li>"name" - Наименование уровня поддержки</li></ol>',
        responses = {(200, 'application/json'): OpenApiResponse(response = SupportLevelSerializer(many = True))}
    )
    def get(self, request, *args, **kwargs):
        levels = SupportLevelModel.objects.all()
        serializer = SupportLevelSerializer(levels, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Добавление уровня поддержки',
        description = '<ol><li>"priority" - Приоритет отображения уровня (упорядочивание от меньшего к большему)</li>\
        <li>"name" - Наименование уровня поддержки</li></ol>',
        request = SupportLevelSerializer(),
        responses = {(201, 'application/json'): OpenApiResponse(response = SupportLevelSerializer())}
    )
    def post(self, request, *args, **kwargs):
        serializer = SupportLevelSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags = ['Уровни поддержки (Done)']
)
class SupportLevelEditAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Детальная информация об уровне поддержки',
        description = '<ol><li>"id" - Идентификатор уровня поддержки</li>\
        <li>"priority" - Приоритет отображения уровня (упорядочивание от меньшего к большему)</li>\
        <li>"name" - Наименование уровня поддержки</li></ol>',
        parameters = [
            OpenApiParameter(name = 'level_id', description = 'Идентификатор уровня поддержки', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = SupportLevelSerializer())}
    )
    def get(self, request, level_id, *args, **kwargs):
        level = GetSupportLevel(level_id)
        serializer = SupportLevelSerializer(level)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Изменение уровня поддержки',
        request = SupportLevelSerializer(),
        description = '<ol><li>"priority" - Приоритет отображения уровня (упорядочивание от меньшего к большему)</li>\
        <li>"name" - Наименование уровня поддержки</li></ol>',
        parameters = [
            OpenApiParameter(name = 'level_id', description = 'Идентификатор уровня поддержки', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = SupportLevelSerializer())}
    )
    def put(self, request, level_id, *args, **kwargs):
        level = GetSupportLevel(level_id)
        serializer = SupportLevelSerializer(level, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление уровня поддержки',
        parameters = [
            OpenApiParameter(name = 'level_id', description = 'Идентификатор уровня поддержки', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элемент удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Элемент удален'})])}
    )
    def delete(self, request, level_id, *args, **kwargs):
        level = GetSupportLevel(level_id)
        level.delete()
        return Response({'message': 'Элемент удален'}, status = status.HTTP_200_OK)

def GetSupportLevel(level_id):
    try:
        return SupportLevelModel.objects.get(id = level_id)
    except:
        raise APIException('Уровень поддержки с id = ' + str(level_id) + ' не найден')

@extend_schema(
    tags = ['Договоры (Done)']
)
class ContractsListAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        summary = 'Список договоров',
        description = '<ol><li>"id" - Идентификатор договора</li>\
        <li>"number" - Номер договора</li><li>"organization_name" - Наименование организации</li></ol>',
        responses = {(200, 'application/json'): OpenApiResponse(response = ContractListSerializer(many = True))}
    )
    def get(self, request, *args, **kwargs):
        contracts = ContractModel.objects.annotate(organization_name = F('client__organization__name')).values('id', 'number', 'organization_name')

        return Response(contracts, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Добавление договора',
        description = '<ol><li>"number" - Номер договора</li><li>"client" - Идентификатор поставщика</li>\
        <li>"end_user" - Идентификатор конечного пользователя</li><li>"dc_address" - Адрес ЦОД</li>\
        <li>"signed" - Дата начала договора <b>в формате dd.mm.yyyy</b></li><li>"enddate" - Дата окончания договора <b>в формате dd.mm.yyyy</b></li>\
        <li>"link" - Ссылка на договор</li><li>"eqcontracts" - Список оборудования договора, где<ul>\
        <li>"id" - Идентификатор привязки оборудования к договору <b>(Не используется в данном методе, указывать не нужно)</b></li>\
        <li>"sn" - Серийный номер оборудования</li><li>"equipment" - Идентификатор оборудования</li>\
        <li>"support" - Идентификатор уровня поддержки</li><li>"DELETE" - True, если необходимо убрать привязку оборудования к договору</li></ul></li></ol>',
        request = ContractDetailsSerializer(),
        responses = {(201, 'application/json'): OpenApiResponse(response = ContractDetailsSerializer())}
    )
    def post(self, request, *args, **kwargs):
        serializer = ContractDetailsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Элемент создан'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags = ['Договоры (Done)']
)
class ContractsEditAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        summary = 'Детальная информация о договоре',
        description = '<ol><li>"id" - Идентификатор договора</li><li>"number" - Номер договора</li><li>"client" - Идентификатор поставщика</li>\
        <li>"end_user" - Идентификатор конечного пользователя</li><li>"dc_address" - Адрес ЦОД</li>\
        <li>"signed" - Дата начала договора в формате dd.mm.yyyy</li><li>"enddate" - Дата окончания договора в формате dd.mm.yyyy</li>\
        <li>"link" - Ссылка на договор</li><li>"eqcontracts" - Список оборудования договора, где<ul>\
        <li>"id" - Идентификатор привязки оборудования к договору</li>\
        <li>"sn" - Серийный номер оборудования</li><li>"equipment" - Идентификатор оборудования</li>\
        <li>"support" - Идентификатор уровня поддержки</li><li>"DELETE" - True, если необходимо убрать привязку оборудования к договору <b>(Не используется в данном методе)</b></li></ul></li></ol>',
        parameters = [
            OpenApiParameter(name = 'contract_id', description = 'Идентификатор договора', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = ContractDetailsSerializer())}
    )
    def get(self, request, contract_id, *args, **kwargs):
        contract = GetContract(contract_id)
        serializer = ContractDetailsSerializer(contract)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Изменение договора',
        description = '<ol><li>"number" - Номер договора</li><li>"client" - Идентификатор поставщика</li>\
        <li>"end_user" - Идентификатор конечного пользователя</li><li>"dc_address" - Адрес ЦОД</li>\
        <li>"signed" - Дата начала договора <b>в формате dd.mm.yyyy</b></li><li>"enddate" - Дата окончания договора <b>в формате dd.mm.yyyy</b></li>\
        <li>"link" - Ссылка на договор</li><li>"eqcontracts" - Список оборудования договора, где<ul>\
        <li>"id" - Идентификатор привязки оборудования к договору <b>(Указывется в случае изменения / удаления уже существующей привязки)</b></li>\
        <li>"sn" - Серийный номер оборудования</li><li>"equipment" - Идентификатор оборудования</li>\
        <li>"support" - Идентификатор уровня поддержки</li><li>"DELETE" - True, если необходимо убрать привязку оборудования к договору</li></ul></li></ol>',
        parameters = [
            OpenApiParameter(name = 'contract_id', description = 'Идентификатор договора', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        request = ContractDetailsSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = ContractDetailsSerializer())}
    )
    def put(self, request, contract_id, *args, **kwargs):
        contract = GetContract(contract_id)
        serializer = ContractDetailsSerializer(contract, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary = 'Удаление договора',
        parameters = [
            OpenApiParameter(name = 'contract_id', description = 'Идентификатор договора', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элемент удален'}, examples = [OpenApiExample('Пример', value = {'message': 'Элемент удален'})])}
    )
    def delete(self, request, contract_id, *args, **kwargs):
        contract = GetContract(contract_id)
        contract.delete()
        return Response({'message': 'Элемент удален'}, status = status.HTTP_200_OK)

@extend_schema(
    tags = ['Договоры (Done)']
)
class ContractsDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        summary = 'Удаление списка договоров',
        description = 'Используется метод POST, т.к. методом DELETE невозможно отправить тело запроса\
        <p>"id" - Список идентификаторов договоров { "id": [1, 2, 3] }</p>',
        request = ContractsDeleteSerializer(),
        responses = {(200, 'application/json'): OpenApiResponse(response = {'message': 'Элементы удалены'}, examples = [OpenApiExample('Пример', value = {'message': 'Элементы удалены'})])}
    )
    def post(self, request, *args, **kwargs):
        serializer = ContractsDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            ContractModel.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status=status.HTTP_400_BAD_REQUEST)

def GetContract(contract_id):
    try:
        contract = ContractModel.objects.prefetch_related('eqcontracts').get(id = contract_id)
    except Snippet.DoesNotExist:
        return Response({'message': 'DoesNotExist'}, status = status.HTTP_400_BAD_REQUEST)
    return contract
