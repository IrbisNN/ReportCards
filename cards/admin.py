from django.contrib import admin
from .models import School, Student, Teacher, Parent, Grade, Subject, Classe, StudentSchool, StudentGrade, StudentClasse, TeacherSchool, TeacherClasse, ParentStudent, TeacherSubject, Schedule, FixedSchedule, FixedScheduleDetail

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StudentSchoolInline(admin.TabularInline):
    model = StudentSchool

class TeacherSchoolInline(admin.TabularInline):
    model = TeacherSchool

class TeacherSubjectInline(admin.TabularInline):
    model = TeacherSubject

class ParentStudentInline(admin.TabularInline):
    model = ParentStudent

class StudentClasseInline(admin.TabularInline):
    model = StudentClasse

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['account__first_name', 'account__last_name', 'full_name']
    list_filter = ['account__user__is_active']
    autocomplete_fields = ['account']
    inlines = [
        StudentSchoolInline,
        StudentClasseInline,
    ]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['account__first_name', 'account__last_name']
    autocomplete_fields = ['account']
    inlines = [
        TeacherSchoolInline,
        TeacherSubjectInline,
    ]

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['account__first_name', 'account__last_name']
    autocomplete_fields = ['account']
    inlines = [
        ParentStudentInline,
    ]

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Classe)
admin.site.register(StudentSchool)
admin.site.register(StudentGrade)
admin.site.register(StudentClasse)
admin.site.register(TeacherSchool)

@admin.register(TeacherClasse)
class TeacherClasseAdmin(admin.ModelAdmin):
    search_fields = ['teacher__account__first_name', 'teacher__account__last_name']
    list_display = ['teacher__account__first_name', 'teacher__account__last_name', 'classId__name', 'isHeadTeacher']

admin.site.register(ParentStudent)
admin.site.register(TeacherSubject)
admin.site.register(Schedule)
admin.site.register(FixedSchedule)
admin.site.register(FixedScheduleDetail)
