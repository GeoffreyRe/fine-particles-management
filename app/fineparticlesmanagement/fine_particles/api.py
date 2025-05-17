from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Measurement, Unit, MeasurementType
from .serializers import MeasurementSerializer

@api_view(['POST'])
def create_measurement(request):
    if request.method == 'POST':
        unit_name = request.data.get('unit')
        type_name = request.data.get('type')
        value = request.data.get('value')
        time = request.data.get('time')

        unit = Unit.objects.get(name=unit_name)
        measurement_type = MeasurementType.objects.get(name=type_name)

        measurement = Measurement.objects.create(
            unit=unit,
            type=measurement_type,
            value=value,
            time=time
        )

        serializer = MeasurementSerializer(measurement)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_measurements(request):
    if request.method == 'GET':
        # Optimisation de la récupération des mesures et de leurs objets associés
        measurements = Measurement.objects.all().select_related('unit', 'type')
        
        # Sérialisation des données avec many=True
        serializer = MeasurementSerializer(measurements, many=True)
        
        # Retourner les données avec un statut 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)