from django import forms
from .models import FD

class FDForm(forms.ModelForm):
    class Meta:
        model = FD
        fields = '__all__'