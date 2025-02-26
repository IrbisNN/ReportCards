from django.contrib import admin
from .models import School
from .models import Student
from .models import Teacher
from .models import Parent
from .models import Grade
from .models import Subject
from .models import Classe
from .models import StudentGrade
from .models import StudentClasse
from .models import TeacherClasse
from .models import ParentStudent
from .models import TeacherSubject
from .models import Schedule

admin.site.register(School)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Classe)
admin.site.register(StudentGrade)
admin.site.register(StudentClasse)
admin.site.register(TeacherClasse)
admin.site.register(ParentStudent)
admin.site.register(TeacherSubject)
admin.site.register(Schedule)
