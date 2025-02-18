from rest_framework import serializers

from equipments.models import EquipmentModel, TypeModel, VendorModel, BrandModel, ModelModel

class EquipmentsListSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(label = 'Наименование типа')
    vendor_name = serializers.CharField(label = 'Наименование вендора')
    brand_name = serializers.CharField(label = 'Наименование бренда')
<<<<<<< HEAD
    model_name = serializers.CharField(label = 'Наименование модель')
=======
    model_name = serializers.CharField(label = 'Наименование модели')
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10

    class Meta:
        model = EquipmentModel
        fields = ['id', 'type_name', 'vendor_name', 'brand_name', 'model_name']

class EditEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = '__all__'

class EquipmentsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = EquipmentModel
        fields = ['id']

class EquipmentImportSerializer(serializers.Serializer):
    excel = serializers.FileField(label = 'Файл для загрузки', required = True)

#Типы оборудования
class EquipmentTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeModel
        fields = '__all__'

class EquipmentTypesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = TypeModel
        fields = ['id']

#Вендоры оборудования
class EquipmentVendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = '__all__'

class EquipmentVendorsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = VendorModel
        fields = ['id']

#Бренды оборудования
class EquipmentBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = '__all__'

class EquipmentBrandsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = BrandModel
        fields = ['id']

#Модели оборудования
class EquipmentModelsSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(label = 'Наименование вендора')
    brand_name = serializers.CharField(label = 'Наименование бренда')

    class Meta:
        model = ModelModel
        fields = ['id', 'name', 'brand_name', 'vendor_name']

class EditEquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelModel
        fields = '__all__'

class EquipmentModelsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = ModelModel
        fields = ['id']
