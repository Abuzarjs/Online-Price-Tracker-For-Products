from django import forms
from .models import PriceTracker

class PriceTrackerForm(forms.ModelForm):
    class Meta:
        model = PriceTracker
        fields = ['url', 'desired_price', 'alert_time','email']
