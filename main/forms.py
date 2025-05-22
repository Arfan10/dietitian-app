from django import forms 
from .models import Appointment
from datetime import date

class AppointmentForm(forms.ModelForm):
    time = forms.CharField(required=True)
    
    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'hidden', # Hide native date picker since we're using Pikaday
                'min': date.today().strftime('%Y-%m-%d'), # Only allow future dates
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Any special requirements or information...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Make all fields required except message
        for field_name, field in self.fields.items():
            if field_name != 'message':
                field.required = True
                
    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        today = date.today()
        
        if selected_date < today:
            raise forms.ValidationError("Appointments cannot be booked in the past.")
        
        return selected_date