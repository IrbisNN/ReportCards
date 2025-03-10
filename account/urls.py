from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
] + debug_toolbar_urls()