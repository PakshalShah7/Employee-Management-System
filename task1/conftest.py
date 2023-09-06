""" This file contains fixtures which can be used to get some data to the tests. """

from typing import List, Any
import pytest
from task1.factories import SkillFactory, EmployeeFactory, EmployeeSkillFactory
from task1.models import Skill, Employee


@pytest.fixture
def create_skill() -> Skill:
    """
    This method should create fixture for Skill.
    """
    factory = SkillFactory.create()
    return factory


@pytest.fixture
def create_employee() -> Employee:
    """
    This method should create fixture for Employee.
    """
    factory = EmployeeFactory.create()
    return factory


@pytest.fixture
def create_employee_skill(create_employee) -> List[Any]:
    """
    This method should create fixture for EmployeeSkill.
    """
    factory_list = []
    for emp_skill in range(2):
        factory_list.append(EmployeeSkillFactory(employee=create_employee))
    return factory_list
