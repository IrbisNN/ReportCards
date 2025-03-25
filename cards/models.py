from django.db import models
from account.models import Account
from django.urls import reverse
from django.template.defaultfilters import slugify

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cards:school_detail', args=[self.id])

    def change_name(self, school, name):
        school.name = name
        school.save()

class Student(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, null=True)

    def __str__(self):
        return f'{self.account.first_name} {self.account.last_name}'
    
    def full_name(self):
        return self.account.first_name + " " + self.account.last_name

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
        return self.account.first_name + " " + self.account.last_name

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

    def __str__(self):
        return self.name

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

class Schedule(models.Model):
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    weekDay = models.IntegerField()
    year = models.IntegerField()