from django.db import models
from account.models import Account
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cards:school_detail', args=[self.id])

    def change_name(self, name):
        self.name = name
        self.save()

    def get_schedule(self):
        fixed_schedule = FixedSchedule.objects.filter(school=self)
        return fixed_schedule

    def get_schedule_byclasse(self, classe):
        fixed_schedule = FixedSchedule.objects.filter(school=self, classId=classe)
        return fixed_schedule

class Student(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, null=True)

    def __str__(self):
        return f'{self.account.first_name} {self.account.last_name}'
    
    def full_name(self):
        return f'{self.account.first_name} {self.account.last_name}'

    def get_absolute_url(self):
        return reverse('cards:student_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.account.first_name}-{self.account.last_name}')
        super(Student, self).save(*args, **kwargs)

class Teacher(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, null=True)

    def __str__(self):
        return f'{self.account.first_name} {self.account.last_name}'

    def full_name(self):
        return f'{self.account.first_name} {self.account.last_name}'

    def short_name(self):
        return f'{self.account.last_name} {self.account.first_name[0]}.'

    def get_absolute_url(self):
        return reverse('cards:teacher_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.account.first_name}-{self.account.last_name}')
        super(Teacher, self).save(*args, **kwargs)

class Parent(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.first_name} {self.account.last_name}'

class Grade(models.Model):
    name = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['value']

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Classe(models.Model):
    name = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} - {self.school.name}'

class StudentSchool(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.account.first_name} {self.student.account.last_name} - {self.school.name}'
    
    def student_school_add(self, student, school, classe):
        exist = StudentSchool.objects.filter(student=student, school=school)
        if not exist:
            student = StudentSchool()
            student.student = student
            student.school = school
            student.save()
        classexist = StudentClasse.objects.filter(student=student, school=school)    
        if not classexist:
            classe = StudentClasse()
            classe.student = student
            classe.classId = classe
            classe.school = school
            classe.save()
        else:
            return 'Student already added to school'
    
        return 'Student added to school successfully'

class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.student.account.first_name} {self.student.account.last_name} - {self.date} - {self.subject.name} - {self.grade.name}'
    
    class Meta:
        ordering = ['date']

    def garde_add(self, student, grade, subject, teacher, date):
        newGrade = StudentGrade()
        newGrade.student = student
        newGrade.grade = grade
        newGrade.subject = subject
        newGrade.teacher = teacher
        newGrade.date = date
        newGrade.save()

class StudentClasse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    assignmentDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.account.first_name} {self.student.account.last_name} - {self.school.name} - {self.classId.name}'

class TeacherSchool(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.account.first_name} {self.teacher.account.last_name} - {self.school.name}'

    def teacher_school_add(self, teacher, school):
        exist = TeacherSchool.objects.filter(teacher=teacher, school=school)
        if exist:
            return 'Teacher already assigned to school'
        newTeacherSchool = TeacherSchool()
        newTeacherSchool.teacher = teacher
        newTeacherSchool.school = school
        newTeacherSchool.save()
        return 'Teacher assigned to school successfully'

class TeacherClasse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    isHeadTeacher = models.BooleanField()

    def __str__(self):
        if self.isHeadTeacher:
            return f'{self.classId.name} - Head Teacher'
        else:
            return f'{self.classId.name}'

class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'Parent: {self.parent.account.first_name} {self.parent.account.last_name} - Student: {self.student.account.first_name} {self.student.account.last_name}'
    
    def parent_student_add(self, parent, student):
        exist = ParentStudent.objects.filter(parent=parent, student=student)
        if exist:
            return 'Parent already added'
        newParentStudent = ParentStudent()
        newParentStudent.parent = parent
        newParentStudent.student = student
        newParentStudent.save()
        return 'Parent added successfully'

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.account.first_name} {self.teacher.account.last_name} - {self.subject.name}'

class Weekday(models.IntegerChoices):
    MONDAY = 1, _("Monday")
    THUESDAY = 2, _("Thuesday")
    WEDNESDAY = 3, _("Wednesday")
    THURSDAY = 4, _("Thursday")
    FRIDAY = 5, _("Friday")
    SATURDAY = 6, _("Saturday")
    SUNDAY = 7, _("Sunday")

    __empty__ = _("(Unknown)")

class Daytype(models.TextChoices):
    WEEKDAY = 'W', _("Weekday")
    WEEKEND = 'E', _("Weekend")
    HOLIDAY = 'H', _("Holiday")

    __empty__ = _("(Unknown)")

class Schedule(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    startTime = models.TimeField(null=True)
    duration = models.IntegerField(null=True)
    weekDay = models.IntegerField(null=True, choices=Weekday.choices)
    dayType = models.CharField(max_length=50, null=True, choices=Daytype.choices)

class FixedSchedule(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.school.name} - {self.classId.name} - {self.startDate} - {self.endDate}'
    
class FixedScheduleDetail(models.Model):
    schedule = models.ForeignKey(FixedSchedule, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    weekDay = models.IntegerField(choices=Weekday.choices)
    startTime = models.TimeField()
    duration = models.IntegerField()
    dayType = models.CharField(max_length=50, choices=Daytype.choices)

    def __str__(self):
        return f'{self.startTime} - {self.subject.name} - {self.teacher.account.last_name} {self.teacher.account.last_name[0]}.'

    class Meta:
        ordering = ['startTime']
