from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import School

@login_required
def school_list(request):
    schools = School.objects.all()
    return render(request, 'schools.html', {'schools': schools})

@login_required
def school_detail(request, id):
    school = get_object_or_404(School, id=id)
    return render(request, 'school_detail.html', {'school': school})