from rest_framework import serializers
from .models import Measurement, Unit, MeasurementType

class MeasurementSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source='unit.name')
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Measurement
        fields = ['unit', 'type', 'value', 'time']