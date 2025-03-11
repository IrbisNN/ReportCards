from django.contrib import admin
from .models import School, Student, Teacher, Parent, Grade, Subject, Classe, StudentSchool, StudentGrade, StudentClasse, TeacherSchool, TeacherClasse, ParentStudent, TeacherSubject, Schedule

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SchoolInline(admin.TabularInline):
    model = StudentSchool

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['account__frist_name', 'account__last_name']
    list_display = ['account__frist_name', 'account__last_name', 'full_name']
    autocomplete_fields = ['account']
    inlines = [
        SchoolInline,
    ]

admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Classe)
admin.site.register(StudentSchool)
admin.site.register(StudentGrade)
admin.site.register(StudentClasse)
admin.site.register(TeacherSchool)
admin.site.register(TeacherClasse)
admin.site.register(ParentStudent)
admin.site.register(TeacherSubject)
admin.site.register(Schedule)