from django.urls import path
from .views import MeasurementListView, MeasurementByTypeListView

urlpatterns = [
    path('', MeasurementListView.as_view(), name='measurement_list'),
    path('type/<str:type_name>/', MeasurementByTypeListView.as_view(), name='measurement_by_type'),
]