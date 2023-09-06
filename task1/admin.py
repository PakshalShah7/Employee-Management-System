from django.contrib import admin
from .models import Skill, Employee, EmployeeSkill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    This class will register Skill model in admin site.
    """
    list_display = ['skill_name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    This class will register Employee model in admin site.
    """
    list_display = ['employee_name', 'reporting_manager']


@admin.register(EmployeeSkill)
class EmployeeSkillsAdmin(admin.ModelAdmin):
    """
    This class will register EmployeeSkill model in admin site.
    """
    list_display = ['employee', 'skill', 'rating']
