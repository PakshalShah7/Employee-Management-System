import factory
from .models import Skill, Employee, EmployeeSkill


class SkillFactory(factory.django.DjangoModelFactory):
    """
    This class should create factory which will generate data for Skill model.
    """
    skill_name = factory.Faker('name')

    class Meta:
        model = Skill


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    This class should create factory which will generate data for Employee model.
    """
    employee_name = factory.Faker('name')

    class Meta:
        model = Employee

    @factory.post_generation
    def employee_skill(self, create, extracted, **kwargs):
        """
        This class should create factory for EmployeeSkill model.
        """
        if not create:
            return

        skill = SkillFactory()
        emp_skill = EmployeeSkillFactory(employee=self, skill=skill)
        self.skill.add(skill)


class EmployeeSkillFactory(factory.django.DjangoModelFactory):
    """
    This class should create factory which will generate data for EmployeeSkill model.
    """
    employee = factory.SubFactory(EmployeeFactory)
    skill = factory.SubFactory(SkillFactory)
    description = factory.Faker('name')
    rating = factory.Faker('pyint', min_value=1, max_value=10)

    class Meta:
        model = EmployeeSkill
