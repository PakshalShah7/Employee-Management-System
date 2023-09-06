from http import HTTPStatus
import pytest
from django.urls import reverse
from task1.constants import SKILL_NAME, SKILL_CREATE_URL, SKILL_LIST_URL, SKILL_UPDATE_URL, COUNT_ZERO, \
    COUNT_ONE, SKILL_DELETE_URL, SKILL_UPDATE_NAME, EMPLOYEE_NAME, EMPLOYEE_CREATE_URL, DESCRIPTION, \
    RATING, EMPLOYEE_LIST_URL, EMPLOYEE_UPDATE_NAME, EMPLOYEE_UPDATE_URL, EMPLOYEE_DELETE_URL
from task1.factories import SkillFactory
from task1.models import Skill, Employee, EmployeeSkill

pytestmark = pytest.mark.django_db


class TestSkill:
    """
    This class contains all test cases of Skill model.
    """

    def test_create_skill_successfully(self, client):
        """
        This method should test that skill is created successfully.
        """
        data = {
            'skill_name': SKILL_NAME
        }
        response = client.post(reverse(SKILL_CREATE_URL), data)
        assert response.status_code == HTTPStatus.FOUND
        assert Skill.objects.filter(skill_name=SKILL_NAME).exists()

    def test_create_skill_form_field_error(self, client):
        """
        This method should test that it displays form field error if skill name is not entered.
        """
        assert not Skill.objects.count() == 1
        data = {
            'skill_name': ''
        }
        response = client.post(reverse(SKILL_CREATE_URL), data)
        assert list(response.context['form'].errors.values())[0][0] == 'This field is required.'

    def test_skill_list(self, create_skill, client):
        """
        This method should test that it displays the list of skills.
        """
        response = client.get(reverse(SKILL_LIST_URL))
        assert response.status_code == HTTPStatus.OK
        assert len(response.context['skills']) == COUNT_ONE

    def test_skill_update(self, create_skill, client):
        """
        This method should test that it updates the skill name.
        """
        data = {
            'skill_name': SKILL_UPDATE_NAME
        }
        response = client.post(reverse(SKILL_UPDATE_URL, args=[create_skill.pk]), data)
        create_skill.refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert create_skill.skill_name == SKILL_UPDATE_NAME
        assert Skill.objects.filter(skill_name=SKILL_UPDATE_NAME).exists()

    def test_update_skill_form_field_errors(self, create_skill, client):
        """
        This method should test that it displays form field error if invalid data is entered.
        """
        data = {
            'abc': 'xyz'
        }
        response = client.post(reverse(SKILL_UPDATE_URL, args=[create_skill.pk]), data)
        assert response.status_code == HTTPStatus.OK
        assert list(response.context['form'].errors.values())[0][0] == 'This field is required.'

    def test_skill_delete(self, create_skill, client):
        """
        This method should test that it deletes the skill.
        """
        response = client.post(reverse(SKILL_DELETE_URL, args=[create_skill.pk]))
        assert response.status_code == HTTPStatus.FOUND
        assert not Skill.objects.filter(id=create_skill.pk).exists()


class TestEmployee:
    """
    This class contains all test cases of Employee model.
    """

    def test_employee_list(self, create_employee, client):
        """
        This method should test that it displays the list of employees.
        """
        response = client.get(reverse(EMPLOYEE_LIST_URL))
        assert response.status_code == HTTPStatus.OK
        assert response.context['employees'].count() == COUNT_ONE

    def test_search_employee(self, create_employee, client):
        """
        This method should test that it search out the employee.
        """
        data = {
            'search': create_employee.employee_name
        }
        response = client.get(reverse(EMPLOYEE_LIST_URL), data)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context['employees']) == COUNT_ONE

    def test_search_invalid_employee(self, client):
        """
        This method should test that it returns 'no result found' if invalid data is searched.
        """
        data = {
            'search': EMPLOYEE_UPDATE_NAME
        }
        response = client.get(reverse(EMPLOYEE_LIST_URL), data)
        assert len(response.context['employees']) == COUNT_ZERO

    def test_employee_update(self, create_employee, client):
        """
        This method should test that it updates the employee name.
        """
        data = {
            'employee_name': EMPLOYEE_UPDATE_NAME
        }
        response = client.post(reverse(EMPLOYEE_UPDATE_URL, args=[create_employee.pk]), data)
        create_employee.refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert create_employee.employee_name == EMPLOYEE_UPDATE_NAME
        assert Employee.objects.filter(employee_name=EMPLOYEE_UPDATE_NAME).exists()

    def test_delete_employee(self, create_employee, client):
        """
        This method should test that it deletes the employee.
        """
        response = client.post(reverse(EMPLOYEE_DELETE_URL, args=[create_employee.pk]))
        assert response.status_code == HTTPStatus.FOUND
        assert not Employee.objects.filter(id=create_employee.pk).exists()


class TestEmployeeSkill:
    """
    Ths class contains all test cases of EmployeeSkill model.
    """

    def test_formset_validation(self, create_skill, client):
        """
        This method should test that it creates employee with employee's skills.
        """
        assert not EmployeeSkill.objects.count() == 1
        data = {
            'employees-TOTAL_FORMS': '1',
            'employees-INITIAL_FORMS': '0',
            'employee_name': EMPLOYEE_NAME,
            'employees-0-skill': Skill.objects.first().id,
            'employees-0-description': DESCRIPTION,
            'employees-0-rating': RATING
        }
        response = client.post(reverse(EMPLOYEE_CREATE_URL), data)
        assert response.status_code == HTTPStatus.FOUND
        assert Employee.objects.filter(employee_name=EMPLOYEE_NAME).exists()
        assert EmployeeSkill.objects.filter(description=DESCRIPTION).exists()

    def test_employee_update(self, create_employee_skill, client):
        """
        This method should test that it updates the employee's skills.
        """
        data = {
            'employees-TOTAL_FORMS': '2',
            'employees-INITIAL_FORMS': '1',
            'employees-MIN_NUM_FORMS': ['0'],
            'employees-MAX_NUM_FORMS': ['1000'],
            'employee_name': EMPLOYEE_UPDATE_NAME,
            'employees-0-id': create_employee_skill[0].id,
            'employees-0-skill': create_employee_skill[0].skill.id,
            'employees-0-employee': create_employee_skill[0].employee.id,
            'employees-0-description': DESCRIPTION,
            'employees-0-rating': RATING
        }
        response = client.post(reverse(EMPLOYEE_UPDATE_URL, args=[create_employee_skill[0].employee.pk]),
                               data)
        create_employee_skill[0].refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert create_employee_skill[0].skill.skill_name == create_employee_skill[0].skill.skill_name
        assert create_employee_skill[0].description == DESCRIPTION
        assert create_employee_skill[0].rating == RATING

    def test_employee_update_with_two_input_data(self, create_employee_skill,  client):
        """
        This method should test that it updates two skills of employee.
        """
        skill_1 = SkillFactory()
        skill_2 = SkillFactory()
        data = {
            'employees-TOTAL_FORMS': '3',
            'employees-INITIAL_FORMS': '2',
            'employees-MIN_NUM_FORMS': ['0'],
            'employees-MAX_NUM_FORMS': ['1000'],
            'employee_name': EMPLOYEE_UPDATE_NAME,
            'employees-0-id': create_employee_skill[0].id,
            'employees-0-skill': skill_1.id,
            'employees-0-employee': create_employee_skill[0].employee.id,
            'employees-0-description': DESCRIPTION,
            'employees-0-rating': RATING,
            'employees-1-id': create_employee_skill[1].id,
            'employees-1-skill': skill_2.id,
            'employees-1-employee': create_employee_skill[0].employee.id,
            'employees-1-description': 'Good',
            'employees-1-rating': 8
        }
        response = client.post(reverse(EMPLOYEE_UPDATE_URL, args=[create_employee_skill[0].employee.pk]),
                               data)
        create_employee_skill[0].refresh_from_db()
        create_employee_skill[1].refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert create_employee_skill[0].description == DESCRIPTION
        assert create_employee_skill[0].rating == RATING
        assert create_employee_skill[1].description == 'Good'
        assert create_employee_skill[1].rating == 8
