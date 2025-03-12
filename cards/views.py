from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import School, Student, StudentSchool, ParentStudent, StudentGrade
from .forms import SchoolForm, GradeAddForm

@login_required
def school_list(request):
    schools = School.objects.all()
    return render(request, 'schools.html', {'schools': schools})

@login_required
def school_detail(request, id):
    school = get_object_or_404(School, id=id)
    school_form = SchoolForm(initial={'name': school.name})
    return render(request, 'school_detail.html', {'school': school, 'school_form': school_form})

@login_required
def school_save(request, id):
    school = get_object_or_404(School, id=id)
    school_form = SchoolForm(request.POST)
    if school_form.is_valid():
        cd = school_form.cleaned_data
        school.name = cd['name']
        school.save()
    return redirect('cards:school_detail', id=id)

@login_required
def student_list(request):
    sudents = Student.objects.filter(account__user__is_active=True)
    return render(request, 'students.html', {'students': sudents})

@login_required
def student_detail(request, id):
    studentOb = get_object_or_404(Student, id=id)
    schools = StudentSchool.objects.filter(student=id)
    parents = ParentStudent.objects.filter(student=id)
    gardes = StudentGrade.objects.filter(student=id)
    return render(request, 'student_detail.html', {'student': studentOb, 'schools': schools, 'parents': parents, 'grades': gardes})

@login_required
def grade_add(request, student_id):
    if request.method == 'GET':
        studentOb = get_object_or_404(Student, id=student_id)
        form = GradeAddForm()
        return render(request, 'grade_add.html', {'form': form, 'student': studentOb})
    elif request.method == 'POST':
        form = GradeAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            grade = StudentGrade()
            grade.student = get_object_or_404(Student, id=student_id)
            # grade.grade = cd['grade']
            # grade.subject = cd['subject']
            # grade.teacher = cd['teacher']
            # grade.date = cd['date']
            grade.save()
            return redirect('cards:student_detail', id=student_id)
        else:
            return render(request, 'grade_add.html', {'form': form, 'student': studentOb})