from django import forms
from .models import School, Student, StudentGrade, TeacherSchool, ParentStudent, StudentSchool, Classe, TeacherSubject, Teacher
from account.models import Account
from django.utils.translation import gettext_lazy as _
from .roles import get_role_choices
from django.forms import inlineformset_factory

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
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = StudentGrade
        fields = ['grade', 'subject', 'teacher', 'date']
        localized_fields = ['date']  

class SchoolTeacherAddForm(forms.ModelForm):
    class Meta:
        model = TeacherSchool
        fields = ['teacher']

class AssignmentForm(forms.Form):
    role = forms.ChoiceField(choices=get_role_choices(), label=_('Role'), widget=forms.Select(), required=True)
    account = forms.ModelChoiceField(queryset=Account.objects.filter(user__is_active=True), label=_('Account'), widget=forms.Select(), required=True)

class ParentStudentAddForm(forms.ModelForm):
    class Meta:
        model = ParentStudent
        fields = ['parent']

class StudentSchoolAddForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Class'), widget=forms.Select(), required=True)
    class Meta:
        model = StudentSchool
        fields = ['student']

SubjectFormSet = inlineformset_factory(Teacher, TeacherSubject, fields=['subject'], extra = 1, can_delete=True)