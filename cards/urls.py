from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('rolesassignment/', views.role_ass, name='role_ass'),
    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:id>/', views.school_detail, name='school_detail'),
    path('schools/save/<int:id>/', views.school_save, name='school_save'),
    path('sudents/', views.student_list, name='student_list'),
    path('sudents/<slug:slug>/', views.student_detail, name='student_detail'),
    path('grades/add/<int:student_id>/', views.grade_add, name='grade_add'),
    path('schools/teachers/add/<int:school_id>/', views.schoolteacher_add, name='schoolteacher_add'),
    path('sudents/parents/add/<int:student_id>/', views.parentstudent_add, name='parentstudent_add'),
    path('schools/students/add/<int:school_id>/', views.schoolstudent_add, name='schoolstudent_add'),
    path('teachers/<slug:slug>/', views.teacher_detail, name='teacher_detail'),
    path('schools/schedule/list/<int:school_id>/', views.schedule_list, name='schedule_list'),
    path('schools/schedule/new/<int:school_id>/', views.schedule_edit, name='schedule_new'),
    path('schools/schedule/edit/<int:school_id>/<int:schedule_id>', views.schedule_edit, name='schedule_edit'),
    path('schools/schedule/addsubject/<int:school_id>/<int:schedule_id>/<int:weekdayId>', views.schedule_add_subject, name='schedule_add_subject'),
]