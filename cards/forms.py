from django import forms
from .models import School

class SchoolForm(forms.Form):
    name = forms.CharField(max_length=100)

    class Meta:
        model = School
        fields = ['name']