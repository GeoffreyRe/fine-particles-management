from django.views.generic import ListView
from .models import Measurement, MeasurementType

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'fine_particles/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        return Measurement.objects.all().order_by('-time', 'type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = MeasurementType.objects.all()
        return context


class MeasurementByTypeListView(ListView):
    model = Measurement
    template_name = 'fine_particles/measurement_list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        type_name = self.kwargs['type_name']
        return Measurement.objects.select_related('unit', 'type').filter(type__name=type_name).order_by('-time', 'type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_type'] = self.kwargs['type_name']
        context['types'] = MeasurementType.objects.all()
        return context
