from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Measurement, MeasurementType
from django.shortcuts import render, redirect
from collections import defaultdict
import json

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

from django.shortcuts import render
from collections import defaultdict
import json
from .models import Measurement  # adapte selon ton modèle

def dashboard(request):
    # Récupérer toutes les mesures avec leur type
    measurements = Measurement.objects.select_related('type').all()

    # Regrouper par type et heure (arrondi à l'heure)
    grouped = defaultdict(lambda: defaultdict(list))
    all_hours = set()

    for m in measurements:
        type_name = m.type.name
        # Arrondir à l'heure (minutes, secondes à 0)
        hour_str = m.time.replace(minute=0, second=0, microsecond=0).isoformat()
        grouped[type_name][hour_str].append(m.value)
        all_hours.add(hour_str)

    sorted_hours = sorted(all_hours)

    colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)', 'rgb(75, 192, 192)']
    datasets = []

    # Calcul de la moyenne par heure
    for index, (type_name, hour_values) in enumerate(grouped.items()):
        values = []
        for hour in sorted_hours:
            vals = hour_values.get(hour, [])
            avg = sum(vals) / len(vals) if vals else None
            values.append(avg)
        datasets.append({
            'label': type_name,
            'data': values,
            'borderColor': colors[index % len(colors)],
            'fill': False,
            'spanGaps': True,
            'tension': 0.3,
        })

    context = {
        'chart_labels': json.dumps(sorted_hours),
        'chart_datasets': json.dumps(datasets),
    }

    return render(request, 'fine_particles/dashboard.html', context)


def redirect_dashboard(request):
    return redirect("/measurements/dashboard/")