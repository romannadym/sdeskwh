from rest_framework import serializers

from contracts.models import SupportLevelModel, ContractModel, ContractEquipmentModel

class SupportLevelSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField(default = 0)
    class Meta:
        model = SupportLevelModel
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label = 'Идентификатор', required = False)
    DELETE = serializers.BooleanField(label = 'Удалить', default = False, required = False)
    class Meta:
        model = ContractEquipmentModel
        fields = ['id', 'sn', 'equipment', 'support', 'DELETE']

<<<<<<< HEAD
class ContractSerializer(serializers.ModelSerializer):
    eqcontracts = EquipmentSerializer(many = True, required = False)
    signed = serializers.DateField(label = 'Начало договора', format = '%d.%m.%Y')
=======
class ContractDetailsSerializer(serializers.ModelSerializer):
    eqcontracts = EquipmentSerializer(many = True, required = False)
    signed = serializers.DateField(label = 'Начало договора', format = '%d.%m.%Y')
    enddate = serializers.DateField(label = 'Окончание договора', format = '%d.%m.%Y')
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10

    class Meta:
        model = ContractModel
        fields = '__all__'

    def create(self, validated_data):
        equipments = validated_data.pop('eqcontracts')
        contract = ContractModel.objects.create(**validated_data)

        if equipments:
            equipments_instance = []
            for equipment in equipments:
                if not equipment['DELETE']:
                    equipment.pop('DELETE')
                    equipments_instance.append(
                        ContractEquipmentModel(**equipment, contract = contract)
                    )
            ContractEquipmentModel.objects.bulk_create(equipments_instance)

        return contract

    def update(self, instance, validated_data):
        fields = ['number', 'client', 'end_user', 'dc_addres', 'signed', 'enddate', 'link']

        for field in fields:
            setattr(instance, field, validated_data.get(field))
        instance.save()

        equipments = validated_data.pop('eqcontracts')
        if equipments:
            equipments_create = []
            equipments_update = []
            equipments_delete = []
            for equipment in equipments:
                if equipment['DELETE'] and 'id' in equipment.keys():
                    equipments_delete.append(equipment['id'])
                elif not equipment['DELETE']:
                    equipment.pop('DELETE')

                    if 'id' in equipment.keys():
                        equipments_update.append(ContractEquipmentModel(**equipment))
                    else:
                        equipments_create.append(ContractEquipmentModel(**equipment, contract = instance))

            if equipments_delete:
                ContractEquipmentModel.objects.filter(id__in = equipments_delete, contract = instance).delete()
            if equipments_create:
                ContractEquipmentModel.objects.bulk_create(equipments_create, ignore_conflicts = True)
            if equipments_update:
                ContractEquipmentModel.objects.bulk_update(equipments_update, ['equipment', 'sn', 'support'])

            return instance

class ContractsDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField(label = 'Идентификатор', child = serializers.IntegerField(), required = True)
    class Meta:
        model = ContractModel
        fields = ['id']

class ContractListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(label = 'Наименование организации')
    class Meta:
        model = ContractModel
        fields = ['id', 'number', 'organization_name']
