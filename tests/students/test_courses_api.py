from model_bakery import baker
from rest_framework.test import APIClient
import pytest

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        students_set = baker.prepare(Student, _quantity=5)
        return baker.make(Course, students=students_set, *args, **kwargs)

    return factory


def test_something():
    assert True


@pytest.mark.django_db
def test_get_first_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/1/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_get_list_course(client, course_factory, student_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    response = client.get('/api/v1/courses/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_id_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[1].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[1].id


@pytest.mark.django_db
def test_filter_name_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[1].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[1].name


@pytest.mark.django_db
def test_create_course(client, course_factory, student_factory):
    #students = student_factory(_quantity=10)
    response = client.post(f'/api/v1/courses/', data={'name': 'Биология'},
                           format='json')
    assert response.status_code == 201
    data = response.json()
    courses = Course.objects.all()
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_upd_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'Биология'},
                           format='json')
    assert response.status_code == 200
    data = response.json()
    cours = Course.objects.filter(id=courses[0].id)
    assert data['name'] == cours[0].name


@pytest.mark.django_db
def test_del_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
    count = len(courses)
    assert Course.objects.count() == count-1