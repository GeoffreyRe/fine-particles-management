from django.contrib import admin
from .models import Unit, MeasurementType, Measurement

admin.site.register(Unit)
admin.site.register(MeasurementType)
admin.site.register(Measurement)
