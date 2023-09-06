from django.urls import path
from .views import Home, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView, EmployeeDetailView, \
    EmployeeListView, SkillCreateView, SkillUpdateView, SkillDeleteView, SkillListView

app_name = 'task1'

urlpatterns = [


    path('', Home.as_view(), name='home'),

    path('employee_create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee_update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee_delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employee_detail/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee_list/', EmployeeListView.as_view(), name='employee_list'),

    path('skill_create/', SkillCreateView.as_view(), name='skill_create'),
    path('skill_update/<int:pk>/', SkillUpdateView.as_view(), name='skill_update'),
    path('skill_delete/<int:pk>/', SkillDeleteView.as_view(), name='skill_delete'),
    path('skill_list/', SkillListView.as_view(), name='skill_list'),


]
