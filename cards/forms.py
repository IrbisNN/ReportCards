from django import forms
from .models import School, Student, StudentGrade

class SchoolForm(forms.Form):
    name = forms.CharField(max_length=100)

    class Meta:
        model = School
        fields = ['name']

class StudentForm(forms.Form):
    full_name = forms.CharField(max_length=100)

    class Meta:
        model = Student
        fields = ['full_name']

class GradeAddForm(forms.ModelForm):
    class Meta:
        model = StudentGrade
        fields = ['grade', 'subject', 'teacher', 'date']  