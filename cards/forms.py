from django import forms
from .models import School, Student, StudentGrade, TeacherSchool, ParentStudent, StudentSchool, Classe, TeacherSubject, Teacher, FixedSchedule, FixedScheduleDetail
from account.models import Account
from django.utils.translation import gettext_lazy as _
from .roles import get_role_choices
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
import datetime

class SchoolForm(forms.ModelForm):
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

class ScheduleEditForm(forms.Form):
    weekDay = forms.ChoiceField(choices=[(1, 'Monday'), (2, 'Thuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], label=_('Week Day'), widget=forms.Select(), required=True)
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label=_('Start Time'), required=True)
    duration = forms.IntegerField(label=_('Duration'), required=True)
    dayType = forms.ChoiceField(choices=[('W', 'Weekday'), ('E', 'Weekend'), ('H', 'Holiday')], label=_('Day Type'), widget=forms.Select(), required=True)
    subject = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Subject'), widget=forms.Select(), required=True)
    teacher = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Teacher'), widget=forms.Select(), required=True)
    classId = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Class'), widget=forms.Select(), required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label=_('Date'), required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all(), label=_('School'), widget=forms.Select(), required=True)

class FixedScheduleAddForm(forms.ModelForm):
    weekDay = forms.ChoiceField(choices=[(1, 'Monday'), (2, 'Thuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], label=_('Week Day'), widget=forms.Select(), required=True)
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label=_('Start Time'), required=True)
    duration = forms.IntegerField(label=_('Duration'), required=True)
    dayType = forms.ChoiceField(choices=[('W', 'Weekday'), ('E', 'Weekend'), ('H', 'Holiday')], label=_('Day Type'), widget=forms.Select(), required=True)
    subject = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Subject'), widget=forms.Select(), required=True)
    teacher = forms.ModelChoiceField(queryset=Classe.objects.all(), label=_('Teacher'), widget=forms.Select(), required=True)

    class Meta:
        model = FixedSchedule
        fields = ['weekDay', 'startTime', 'duration', 'dayType', 'subject', 'teacher', 'classId', 'school']
        widgets = {
            'weekDay': forms.Select(attrs={'class': 'form-control'}),
            'startTime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'dayType': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class FixedScheduleForm(forms.ModelForm):
    class Meta:
        model = FixedSchedule
        fields = ['classId', 'startDate', 'endDate', 'isActive']

class FixedScheduleDetailForm(forms.ModelForm):
    class Meta:
        model = FixedScheduleDetail
        fields = ['subject', 'teacher', 'startTime', 'duration', 'dayType']

FixedScheduleDetailFormSet = inlineformset_factory(
    FixedSchedule,
    FixedScheduleDetail,
    form=FixedScheduleDetailForm,
    extra=2,
    can_delete=True
)
