# Django
from django import forms
from multiselectfield import MultiSelectField

# local Django
from .models import Alumni

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = [
            'first_name', 'last_name',  'email', 'permanent_address',
            'current_country','current_state', 'current_city', 'phone_number',
            'links','area_of_expertise','about','profile_pic'
        ]

