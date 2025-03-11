from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:id>/', views.school_detail, name='school_detail'),
    path('schools/save/<int:id>/', views.school_save, name='school_save'),
]