from django.urls import path
from .views import MeasurementListView, MeasurementByTypeListView
from . import api
from . import views

urlpatterns = [
    path('', MeasurementListView.as_view(), name='measurement_list'),
    path('type/<str:type_name>/', MeasurementByTypeListView.as_view(), name='measurement_by_type'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

api_urlpatterns = [
     path('', api.create_measurement, name='create_measurement'),
     path('/all', api.get_measurements, name="get_measurements")
]