""" This file contains all the forms which are used in the project. """

from django import forms
from django.forms import inlineformset_factory
from .models import Employee, Skill, EmployeeSkill


class EmployeeForm(forms.ModelForm):
    """
    This Model form will display form to create employee.
    """

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Employee
        fields = ['employee_name', 'reporting_manager']


class SkillForm(forms.ModelForm):
    """
    This Model form will display form to create skill.
    """

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Skill
        fields = ['skill_name']


class EmployeeSkillForm(forms.ModelForm):
    """
    This Model form will display form to create employee's skill.
    """
    rating = forms.IntegerField(min_value=1, max_value=10)

    def __init__(self, *args, **kwargs):
        super(EmployeeSkillForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'description', 'rating']


SkillFormset = inlineformset_factory(Employee, EmployeeSkill, form=EmployeeSkillForm, extra=1)
