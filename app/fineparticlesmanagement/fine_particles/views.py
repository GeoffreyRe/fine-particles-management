from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Measurement, MeasurementType
from django.shortcuts import render, redirect

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

    def level(self):
        if self.type.name == "PM10":
            if self.value <= 20:
                return "Faible"
            elif self.value <= 40:
                return "Modéré"
            elif self.value <= 50:
                return "Élevé"
            else:
                return "Très élevé"
        elif self.type.name == "PM2.5":
            if self.value <= 10:
                return "Faible"
            elif self.value <= 20:
                return "Modéré"
            elif self.value <= 25:
                return "Élevé"
            else:
                return "Très élevé"
        return "Inconnu"

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

def dashboard(request):
    return render(request, 'fine_particles/dashboard.html')    

def redirect_dashboard(request):
    return redirect("/measurements/dashboard/")