from tempfile import NamedTemporaryFile

from django.db.models.functions import Concat, Trim
from django.db.models import Value, Subquery, OuterRef
from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_spectacular.utils import extend_schema

from openpyxl import Workbook, load_workbook
from openpyxl.utils.cell import get_column_letter
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import NamedStyle, Side, Font, Border, Alignment

from integrator.apps.parsers import NestedMultipartParser

from spares.api.serializers import *

from spares.models import SpareModel, PartNumberModel, SparePNModel

#Запчасти
class SparesListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        tags = ['Список запчастей (Done)'],
    )
    def get(self, request, *args, **kwargs):
        spares = SpareModel.objects.all()\
            .annotate(
                spare = Trim(Concat('name', Value(' (S/n: '), 'sn', Value(')')))
            )

        serializer = SparesSerializer(spares, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class SparesListAdminAPIView(APIView):
    permission_classes = [IsAdminUser,]
    parser_classes = [JSONParser, NestedMultipartParser]

    @extend_schema(
        tags = ['Список запчастей. Администрирование (Done)'],
    )
    def get(self, request, *args, **kwargs):
        spares = SpareModel.objects.all()\
            .annotate(
                pn = Subquery(SparePNModel.objects.filter(spare_id = OuterRef('id'))[:1].values('number__number'))
            )

        serializer = SparesAdminSerializer(spares, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Создание (Done)'],
        request = EditSpareSerializer()
    )
    def post(self, request, *args, **kwargs):
        serializer = EditSpareSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class SparesExcelAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Экспорт (Done)'],
    )
    def get(self, request, *args, **kwargs):
        spares = SparesListAdminAPIView().get(request = request).data

        stream = ExportItems(spares, ['Наименование', 'Серийный номер', 'Описание', 'Партномер'], 'ЗИП')

        response = HttpResponse(content = stream, content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=zip.xlsx'
        return response

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Импорт (Done)'],
        request = SparesImportSerializer()
    )
    def post(self, request, *args, **kwargs):
        wb = load_workbook(filename = request.data.get('excel').file)

        sheets = wb.sheetnames
        ws = wb[sheets[0]]
        start = 0
        end = ws.max_row
        records = []

        for m in range(3 , end + 1):
            sp, created = SpareModel.objects.update_or_create(sn = ws.cell(m, 3).value, defaults = {'name': ws.cell(m, 2).value, 'description': ws.cell(m, 4).value})

            if ws.cell(m, 5).value:
                temp = ws.cell(m, 5).value.splitlines()
            if temp:
                for ln in temp:
                    nm, created = PartNumberModel.objects.get_or_create(number = ln)
                    records.append({'spare': sp, 'number': nm})

        list = [SparePNModel(**vals) for vals in records]
        SparePNModel.objects.bulk_create(list, ignore_conflicts = True)
        return Response(records, status = status.HTTP_200_OK)

class SpareEditAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Изменение (Done)'],
        request = EditSpareSerializer()
    )
    def put(self, request, spare_id, *args, **kwargs):
        spare = GetSpare(spare_id)
        serializer = EditSpareSerializer(spare, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Удаление (Done)'],
    )
    def delete(self, request, spare_id, *args, **kwargs):
        spare = GetSpare(spare_id)
        spare.delete()
        return Response({'message': 'Элемент удален'}, status = status.HTTP_200_OK)

class SparesDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список запчастей. Администрирование. Удаление нескольких (Done)'],
        request = SparesDeleteSerializer(),
    )
    def post(self, request, *args, **kwargs):
        serializer = SparesDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            SpareModel.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status=status.HTTP_400_BAD_REQUEST)

def GetSpare(spare_id):
    try:
        return SpareModel.objects.get(id = spare_id)
    except:
        return Response({'message': 'Объект не найден'}, status = status.HTTP_400_BAD_REQUEST)

#Партномера
class PartNumberListAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список партномеров. Администрирование (Done)'],
    )
    def get(self, request, *args, **kwargs):
        pns = PartNumberModel.objects.all()

        serializer = PartNumberSerializer(pns, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Создание (Done)'],
        request = PartNumberSerializer()
    )
    def post(self, request, *args, **kwargs):
        serializer = PartNumberSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PartNumberEditAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Изменение (Done)'],
        request = PartNumberSerializer()
    )
    def put(self, request, pn_id, *args, **kwargs):
        pn = GetPartNumber(pn_id)
        serializer = PartNumberSerializer(pn, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Удаление (Done)'],
    )
    def delete(self, request, pn_id, *args, **kwargs):
        pn = GetPartNumber(pn_id)
        pn.delete()
        return Response({'message': 'Элемент удален'}, status = status.HTTP_200_OK)

class PartNumbersDeleteAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Удаление нескольких (Done)'],
        request = PartNumbersDeleteSerializer(),
    )
    def post(self, request, *args, **kwargs):
        serializer = PartNumbersDeleteSerializer({'id': request.data.getlist('id')})
        if serializer:
            PartNumberModel.objects.filter(id__in = serializer.data.get('id')).delete()
            return Response({'message': 'Элементы удалены'}, status = status.HTTP_200_OK)
        return Response({'error': 'Некорректные данные'}, status = status.HTTP_400_BAD_REQUEST)

class PartNumbersExcelAPIView(APIView):
    permission_classes = [IsAdminUser,]

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Экспорт (Done)'],
    )
    def get(self, request, *args, **kwargs):
        pns = PartNumberListAPIView().get(request = request).data
        fields = ['Партномер',]

        stream = ExportItems(pns, fields, 'Партномера')

        response = HttpResponse(content = stream, content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=partnumbers.xlsx'
        return response

    @extend_schema(
        tags = ['Список партномеров. Администрирование. Импорт (In progress)'],
        request = SparesImportSerializer()
    )
    def post(self, request, *args, **kwargs):
        wb = load_workbook(filename = request.data.get('excel').file)

        sheets = wb.sheetnames
        ws = wb[sheets[0]]
        start = 0
        end = ws.max_row
        records = []

        for m in range(3 , end + 1):
            records.append({'number': ws.cell(m, 2).value})

        list = [PartNumberModel(**vals) for vals in records]
        PartNumberModel.objects.bulk_create(list, ignore_conflicts = True)
        return Response(records, status = status.HTTP_200_OK)

def GetPartNumber(pn_id):
    try:
        return PartNumberModel.objects.get(id = pn_id)
    except:
        return Response({'message': 'Объект не найден'}, status = status.HTTP_400_BAD_REQUEST)

def ExportItems(items, fields, title):
    wb = Workbook()
    with NamedTemporaryFile(delete = True) as tmp:
        ws = wb.active
        ws.title = title

        bd = Side(style = 'thin', color = '000000')

        general = NamedStyle(name = 'general')
        general.font = Font(name = 'Times New Roman', size = 14)
        general.border = Border(left = bd, top = bd, right = bd, bottom = bd)
        general.alignment = Alignment(vertical = 'center', wrap_text = True)
        wb.add_named_style(general)

        header = NamedStyle(name = 'header')
        header.font = Font(name = 'Times New Roman', size = 14, bold = True)
        header.border = Border(left = bd, top = bd, right = bd, bottom = bd)
        header.alignment = Alignment(vertical = 'center', horizontal = 'center', wrap_text = True)
        wb.add_named_style(header)

        ws.column_dimensions['A'].width = 10

        ws['A2'] = '#'
        ws['A2'].style = 'header'
        col = 2

        for field in fields:
            cell = ws.cell(row = 2, column = col, value = field)
            ws.column_dimensions[get_column_letter(col)].width = 20
            cell.style = 'header'
            col = col + 1

        for count, item in enumerate(items):
            cell = ws.cell(row = count + 3, column = 1, value = count + 1)
            cell.style = 'general'
            col = 2
            for field in item.keys():
                if not field == 'id':
                    cell = ws.cell(row = count + 3, column = col, value = str(item[field] or ''))
                    cell.style = 'general'
                    col = col + 1

        wb.save(tmp.name)
        tmp.seek(0)
        return tmp.read()
