from django.contrib import admin
from .models import School, Student, Teacher, Parent, Grade, Subject, Classe, StudentSchool, StudentGrade, StudentClasse, TeacherSchool, TeacherClasse, ParentStudent, TeacherSubject, Schedule

admin.site.register(School)
admin.site.register(Student)
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
