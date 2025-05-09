from django.urls import path
from .views import MeasurementListView, MeasurementByTypeListView
from . import api

urlpatterns = [
    path('', MeasurementListView.as_view(), name='measurement_list'),
    path('type/<str:type_name>/', MeasurementByTypeListView.as_view(), name='measurement_by_type'),
]

api_urlpatterns = [
     path('', api.create_measurement, name='create_measurement'),
]