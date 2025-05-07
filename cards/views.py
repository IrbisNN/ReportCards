from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import School, Student, Teacher, Parent, StudentSchool, ParentStudent, StudentGrade, TeacherSchool, StudentSchool, StudentClasse, TeacherClasse, TeacherSubject, Classe, Weekday, FixedSchedule, FixedScheduleDetail
from .forms import SchoolForm, GradeAddForm, SchoolTeacherAddForm, AssignmentForm, ParentStudentAddForm, StudentSchoolAddForm, SubjectFormSet, FixedScheduleForm, FixedScheduleDetailForm
from django.contrib import messages
from .roles import save_role
from django.forms import inlineformset_factory

@login_required
def school_list(request):
    schools = School.objects.all()
    return render(request, 'schools.html', {'schools': schools})

@login_required
def school_detail(request, id):
    school = get_object_or_404(School, id=id)
    school_form = SchoolForm(initial={'name': school.name})
    teachers = TeacherSchool.objects.filter(school=school)
    students = StudentSchool.objects.filter(school=school, student__account__user__is_active=True)
    students_classes = StudentClasse.objects.filter(school=school)

    return render(request,
                  'school_detail.html',
                  {'school': school, 'school_form': school_form, 'teachers': teachers, 'students': students, 'students_classes': students_classes})

@login_required
def school_save(request, id):
    school = get_object_or_404(School, id=id)
    school_form = SchoolForm(request.POST)
    if school_form.is_valid():
        cd = school_form.cleaned_data
        School.change_name(school, cd['name'])
    return redirect('cards:school_detail', id=id)

@login_required
def student_list(request):
    sudents = Student.objects.filter(account__user__is_active=True)
    return render(request, 'students.html', {'students': sudents})

@login_required
def student_detail(request, slug):
    studentOb = get_object_or_404(Student, slug=slug)
    id = studentOb.id
    schools = StudentSchool.objects.filter(student=id)
    parents = ParentStudent.objects.filter(student=id)
    gardes = StudentGrade.objects.filter(student=id)
    return render(request, 'student_detail.html',
                  {'student': studentOb, 'schools': schools, 'parents': parents, 'grades': gardes})

@login_required
def grade_add(request, student_id):
    studentOb = get_object_or_404(Student, id=student_id)
    if request.method == 'GET':
        form = GradeAddForm()
        return render(request, 'grade_add.html', {'form': form, 'student': studentOb})
    elif request.method == 'POST':
        form = GradeAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            StudentGrade.garde_add(studentOb, cd['grade'], cd['subject'], cd['teacher'], cd['date'])
            return redirect('cards:student_detail', slug=studentOb.slug)
        else:
            return render(request, 'grade_add.html', {'form': form, 'student': studentOb})

@login_required        
def schoolteacher_add(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == 'GET':
        form = SchoolTeacherAddForm()
        return render(request, 'schoolteacher_add.html', {'form': form, 'school': school})
    elif request.method == 'POST':
        form = SchoolTeacherAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = TeacherSchool.teacher_school_add(cd['teacher'], school)
            messages.success(request, result)
            return redirect('cards:school_detail', id=school_id)
        else:
            return render(request, 'schoolteacher_add.html', {'form': form, 'school': school})
        
@login_required
def role_ass(request):
    if request.method == 'GET':
        form = AssignmentForm()
        return render(request, 'role_ass.html', {'form': form})
    elif request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = save_role(cd['role'], cd['account'])
            messages.success(request, result)
        return render(request, 'role_ass.html', {'form': form})
    
@login_required        
def parentstudent_add(request, student_id):
    studentOb = get_object_or_404(Student, id=student_id)
    if request.method == 'GET':
        form = ParentStudentAddForm()
        return render(request, 'parentstudent_add.html', {'form': form, 'student': studentOb})
    elif request.method == 'POST':
        form = ParentStudentAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = ParentStudent.parent_student_add(cd['parent'], studentOb)
            messages.success(request, result)
            return redirect('cards:student_detail', slug=studentOb.slug)
        else:
            return render(request, 'parentstudent_add.html', {'form': form, 'student': studentOb})
        
@login_required        
def schoolstudent_add(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == 'GET':
        form = StudentSchoolAddForm()
        return render(request, 'schoolstudent_add.html', {'form': form, 'school': school})
    elif request.method == 'POST':
        form = StudentSchoolAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = StudentSchool.student_school_add(cd['student'], school, cd['classe'])
            messages.success(request, result)
            return redirect('cards:school_detail', id=school_id)
        else:
            return render(request, 'schoolstudent_add.html', {'form': form, 'school': school})
        
@login_required
def teacher_detail(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    id = teacher.id
    schools = TeacherSchool.objects.filter(teacher=id)
    classes = TeacherClasse.objects.filter(teacher=id)
    if request.method == 'POST':
        subjectformset = SubjectFormSet(request.POST, instance=teacher)
        if subjectformset.is_valid():
            subjectformset.save()
    subjectformset = SubjectFormSet(instance=teacher)
    return render(request, 'teacher_detail.html',
                  {'teacher': teacher, 'schools': schools, 'classes': classes, 'subjectformset': subjectformset})

@login_required
def schedule_edit(request, school_id, schedule_id=None):
    school = get_object_or_404(School, id=school_id)
    classes = Classe.objects.filter(school=school)
    week_days = [(day.value, day.label) for day in Weekday]
    if schedule_id:
        fixed_schedule = get_object_or_404(FixedSchedule, id=schedule_id)
        fixed_schedule_details = FixedScheduleDetail.objects.filter(schedule=fixed_schedule)
        if request.method == 'POST':
            form = FixedScheduleForm(request.POST, instance=fixed_schedule)
            if form.is_valid():
                cd = form.cleaned_data
                fixed_schedule.startDate = cd['startDate']
                fixed_schedule.endDate = cd['endDate']
                fixed_schedule.isActive = cd['isActive']
                fixed_schedule.save()
                messages.success(request, "Schedule updated successfully.")
                return redirect('cards:schedule_edit', school_id=school_id, schedule_id=schedule_id)
        else:
            form = FixedScheduleForm(instance=fixed_schedule)
    else:
        fixed_schedule = None
        fixed_schedule_details = None
        if request.method == 'POST':
            form = FixedScheduleForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                fixed_schedule = FixedSchedule.objects.create(school=school, classId=cd['classId'], startDate=cd['startDate'], endDate=cd['endDate'], isActive=cd['isActive'])
                messages.success(request, "Schedule created successfully.")
                return redirect('cards:schedule_edit', school_id=school_id, schedule_id=fixed_schedule.id)
        else:
            form = FixedScheduleForm()
    
    return render(request,
                  'schedule_edit.html',
                  {'school': school, 'week_days': week_days, 'classes': classes, 'fixed_schedule': fixed_schedule, 'schedule_details': fixed_schedule_details, 'form': form})

@login_required
def schedule_list(request, school_id):
    school = get_object_or_404(School, id=school_id)
    classes = Classe.objects.filter(school=school)
    fixed_schedules = school.get_schedule()

    return render(request,
                  'schedule_list.html',
                  {'school': school, 'fixed_schedules': fixed_schedules})

@login_required
def schedule_add_subject(request, school_id, schedule_id, weekdayId):
    school = get_object_or_404(School, id=school_id)
    fixed_schedule = get_object_or_404(FixedSchedule, id=schedule_id)
    week_days = [(day.value, day.label) for day in Weekday]
    weekday = Weekday(weekdayId).label
    if request.method == 'POST':
        form = FixedScheduleDetailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            fixed_schedule_detail = FixedScheduleDetail.objects.create(
                schedule = fixed_schedule,
                subject = cd['subject'],
                teacher = cd['teacher'],
                weekDay = weekdayId,
                startTime = cd['startTime'],
                duration = cd['duration'],
                dayType = cd['dayType']
            )
            fixed_schedule_detail.save()
            messages.success(request, "Schedule updated successfully.")
            return redirect('cards:schedule_edit', school_id=school_id, schedule_id=schedule_id)
        else:
            return render(request, 'schedule_add_subject.html', {'form': form, 'fixed_schedule': fixed_schedule, 'school': school, 'weekdayId': weekdayId, 'weekday': weekday})
    else:
        form = FixedScheduleDetailForm()
        return render(request, 'schedule_add_subject.html', {'form': form, 'fixed_schedule': fixed_schedule, 'school': school, 'weekdayId': weekdayId, 'weekday': weekday})

@login_required
def schedule_delete_subject(request, fixedId):
    fixed_schedule_detail = get_object_or_404(FixedScheduleDetail, id=fixedId)
    fixed_schedule_detail.delete()
    messages.success(request, "Schedule subject deleted successfully.")
    return redirect('cards:schedule_edit', school_id=fixed_schedule_detail.schedule.school.id, schedule_id=fixed_schedule_detail.schedule.id)