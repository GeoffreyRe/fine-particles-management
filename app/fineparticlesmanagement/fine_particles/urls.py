from django.urls import path
from .views import MeasurementListView

urlpatterns = [
    path('', MeasurementListView.as_view(), name='measurement_list'),
]