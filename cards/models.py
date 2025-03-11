from django.db import models
from account.models import Account
from django.urls import reverse

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cards:school_detail', args=[self.id])

class Student(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.frist_name} {self.account.last_name}'
    
    def full_name(self):
        return self.account.frist_name + " " + self.account.last_name

class Teacher(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.frist_name} {self.account.last_name}'

class Parent(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account.frist_name} {self.account.last_name}'

class Grade(models.Model):
    name = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

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
        return f'{self.student.account.frist_name} {self.student.account.last_name} - {self.school.name}'

class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.student.account.frist_name} {self.student.account.last_name} - {self.date} - {self.subject.name} - {self.grade.name}'

class StudentClasse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.account.frist_name} {self.student.account.last_name} - {self.classId.name}'

class TeacherSchool(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.account.frist_name} {self.teacher.account.last_name} - {self.school.name}'

class TeacherClasse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    isHeadTeacher = models.BooleanField()

class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'Parent: {self.parent.account.frist_name} {self.parent.account.last_name} - Student: {self.student.account.frist_name} {self.student.account.last_name}'

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.account.frist_name} {self.teacher.account.last_name} - {self.subject.name}'

class Schedule(models.Model):
    classId = models.ForeignKey(Classe, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    weekDay = models.IntegerField()
    year = models.IntegerField()