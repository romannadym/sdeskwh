from rest_framework import serializers

from spares.models import SpareModel, SparePNModel, PartNumberModel

class SparesSerializer(serializers.ModelSerializer):
    spare = serializers.CharField(label = 'Название', required = False)

    class Meta:
        model = SpareModel
        fields = '__all__'

class SparesAdminSerializer(serializers.ModelSerializer):
    pn = serializers.CharField(label = 'Партномер', required = False)

    class Meta:
        model = SpareModel
        fields = ['id', 'name', 'sn', 'description', 'pn']

class SparePNSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label = 'Идентификатор', required = False)
    DELETE = serializers.BooleanField(label = 'Удалить', default = False, required = False)

    class Meta:
        model = SparePNModel
        fields = ['id', 'number', 'DELETE']

class EditSpareSerializer(serializers.ModelSerializer):
    pnspare = SparePNSerializer(many = True, required = False)

    class Meta:
        model = SpareModel
        fields = ['name', 'sn', 'description', 'pnspare']

    def create(self, validated_data):
        pns = validated_data.pop('pnspare')
        spare = SpareModel.objects.create(**validated_data)

        if pns:
            pns_instance = []
            for pn in pns:
                if not pn['DELETE']:
                    pn.pop('DELETE')
                    pns_instance.append(
                        SparePNModel(**pn, spare = spare)
                    )
            SparePNModel.objects.bulk_create(pns_instance)

        return spare

    def update(self, instance, validated_data):
        fields = ['name', 'sn', 'description']

        for field in fields:
            setattr(instance, field, validated_data.get(field))
        instance.save()

        pns = validated_data.pop('pnspare')
        if pns:
            pns_create = []
            pns_update = []
            pns_delete = []
            for pn in pns:
                if pn['DELETE'] and 'id' in pn.keys():
                    pns_delete.append(pn['id'])
                elif not pn['DELETE']:
                    pn.pop('DELETE')

                    if 'id' in pn.keys():
                        pns_update.append(SparePNModel(**pn))
                    else:
                        pns_create.append(SparePNModel(**pn, spare = instance))

            if pns_delete:
                SparePNModel.objects.filter(id__in = pns_delete, spare = instance).delete()
            if pns_create:
                SparePNModel.objects.bulk_create(pns_create, ignore_conflicts = True)
            if pns_update:
                SparePNModel.objects.bulk_update(pns_update, ['number',])

            return instance

class SparesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = SpareModel
        fields = ['id']

class SparesImportSerializer(serializers.Serializer):
    excel = serializers.FileField(label = 'Файл для загрузки', required = True)

class LoadedSparesLoadedSerializer(serializers.Serializer):#Для документации
    spare = serializers.IntegerField(label = 'Идентификатор запчасти')
    number = serializers.IntegerField(label = 'Идентификатор партномера')

class PartNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartNumberModel
        fields = '__all__'

class PartNumbersDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = PartNumberModel
        fields = ['id']
