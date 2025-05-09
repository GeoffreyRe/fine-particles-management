from django.views.generic import ListView
from .models import Measurement

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'fine_particles/measurement_list.html'
    context_object_name = 'measurements'
