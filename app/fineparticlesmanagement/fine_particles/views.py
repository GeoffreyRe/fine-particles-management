from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Measurement, MeasurementType

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'fine_particles/measurement_list.html'
    context_object_name = 'measurements'  
    paginate_by = 10  

    def get_queryset(self):
        filter_type = self.request.GET.get('type_name', None)
        if filter_type:
            return Measurement.objects.filter(type__name=filter_type).order_by('-time', 'type')
        else:
            return Measurement.objects.all().order_by('-time', 'type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        measurements_list = self.get_queryset()
        paginator = Paginator(measurements_list, self.paginate_by) 
        page_number = self.request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 
        
        context['measurements'] = page_obj  
        context['types'] = MeasurementType.objects.all() 
        context['filter_type'] = self.request.GET.get('type_name', None) 
        context['is_paginated'] = page_obj.has_other_pages()
        return context

class MeasurementByTypeListView(ListView):
    model = Measurement
    template_name = 'fine_particles/measurement_list.html'
    context_object_name = 'measurements'
    paginate_by = 10

    def get_queryset(self):
        type_name = self.kwargs['type_name']
        return Measurement.objects.select_related('unit', 'type').filter(type__name=type_name).order_by('-time', 'type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        measurements_list = self.get_queryset()
        paginator = Paginator(measurements_list, self.paginate_by) 
        page_number = self.request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 

        context['measurements'] = page_obj
        context['filter_type'] = self.kwargs['type_name']
        context['types'] = MeasurementType.objects.all()
        context['is_paginated'] = page_obj.has_other_pages()
        return context