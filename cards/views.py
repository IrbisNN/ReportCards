from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import School
from .forms import SchoolForm

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