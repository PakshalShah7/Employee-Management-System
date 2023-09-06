from django.db import models
from django_extensions.db.models import TimeStampedModel


class Skill(TimeStampedModel):
    """
    This Model will store skill details.
    """
    skill_name = models.CharField(max_length=30)

    def __str__(self):
        """
        Returns skill name.
        """
        return self.skill_name


class Employee(TimeStampedModel):
    """
    This Model will store employee details.
    """
    employee_name = models.CharField(max_length=50)
    reporting_manager = models.ForeignKey('self', on_delete=models.CASCADE, related_name='managers', null=True,
                                          blank=True)
    skill = models.ManyToManyField(Skill, through='EmployeeSkill')

    def __str__(self):
        """
        Returns employee name.
        """
        return f"Employee: {self.employee_name}"


class EmployeeSkill(TimeStampedModel):
    """
    This Model will store employee's skill details.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employees')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skills')
    description = models.TextField(max_length=50)
    rating = models.PositiveIntegerField()

    def __str__(self):
        """
        Returns employee name.
        """
        return self.employee.employee_name
