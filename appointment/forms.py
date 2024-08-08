from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']
        widgets = {
            'date': forms.TextInput(attrs={'id': 'id_date'}),
            'start_time': forms.TextInput(attrs={'id': 'id_start_time'}),
        }
