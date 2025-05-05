from django import forms 
from .models import Appointment

class AppointmentForm (forms.ModelForm):
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M')) 
    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'date', 'time', 'message']