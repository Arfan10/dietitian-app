from django.contrib import admin
from .models import Appointment, Dietplan, Profile

# admin.site.register(Appointment)
admin.site.register(Dietplan)
admin.site.register(Profile)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email','date', 'time', 'message')
    search_fields = ('full_name', 'email','message')
    list_filter = ('date','time')