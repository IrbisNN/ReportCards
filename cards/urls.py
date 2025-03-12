from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:id>/', views.school_detail, name='school_detail'),
    path('schools/save/<int:id>/', views.school_save, name='school_save'),
    path('sudents/', views.student_list, name='student_list'),
    path('sudents/<int:id>/', views.student_detail, name='student_detail'),
    path('grades/add/<int:student_id>/', views.grade_add, name='grade_add'),
]