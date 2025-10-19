"""
Tests for Student API Routes
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime


@pytest.fixture
def admin_token(client):
    """Get admin token for authentication"""
    response = client.post(
        "/api/v1/user/login",
        data={
            "username": "mhmdd400",
            "password": "mhmdd400"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def teacher_token(client):
    """Get teacher token for authentication"""
    response = client.post(
        "/api/v1/user/login",
        data={
            "username": "teacher1",
            "password": "teacher123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return {
        "full_name": "محمد أحمد علي",
        "email": "mohammed@example.com",
        "phone": "+1234567890",
        "birthdate": "2010-05-15T00:00:00",
        "notes": "Test student"
    }


def test_create_student_as_admin(client, admin_token, sample_student_data):
    """Test creating a student as admin"""
    response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "محمد أحمد علي"
    assert data["email"] == "mohammed@example.com"
    assert data["is_active"] is True
    assert "id" in data


def test_create_student_as_teacher_should_fail(client, teacher_token, sample_student_data):
    """Test that teachers cannot create students"""
    response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 403


def test_get_all_students_as_admin(client, admin_token):
    """Test getting all students as admin"""
    response = client.get(
        "/api/v1/students/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "students" in data


def test_get_all_students_as_teacher(client, teacher_token):
    """Test that teachers can view students"""
    response = client.get(
        "/api/v1/students/",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "students" in data


def test_search_students(client, admin_token, sample_student_data):
    """Test searching students by name"""
    # First create a student
    client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Search for the student
    response = client.get(
        "/api/v1/students/search?name=محمد",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("محمد" in student["full_name"] for student in data["students"])


def test_get_student_by_id(client, admin_token, sample_student_data):
    """Test getting a student by ID"""
    # Create a student
    create_response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    student_id = create_response.json()["id"]
    
    # Get the student
    response = client.get(
        f"/api/v1/students/{student_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == student_id
    assert data["full_name"] == "محمد أحمد علي"


def test_update_student(client, admin_token, sample_student_data):
    """Test updating a student"""
    # Create a student
    create_response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    student_id = create_response.json()["id"]
    
    # Update the student
    update_data = {
        "full_name": "أحمد محمد علي",
        "phone": "+9876543210"
    }
    
    response = client.put(
        f"/api/v1/students/{student_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "أحمد محمد علي"
    assert data["phone"] == "+9876543210"


def test_delete_student(client, admin_token, sample_student_data):
    """Test deleting a student (soft delete)"""
    # Create a student
    create_response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    student_id = create_response.json()["id"]
    
    # Delete the student
    response = client.delete(
        f"/api/v1/students/{student_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    # Verify student is marked as inactive
    get_response = client.get(
        f"/api/v1/students/{student_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_response.json()["is_active"] is False


def test_create_student_with_duplicate_email(client, admin_token, sample_student_data):
    """Test creating a student with duplicate email"""
    # Create first student
    client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Try to create another student with same email
    response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_nonexistent_student(client, admin_token):
    """Test getting a student that doesn't exist"""
    response = client.get(
        "/api/v1/students/nonexistent-id",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 404


def test_get_students_include_inactive(client, admin_token, sample_student_data):
    """Test getting students including inactive ones"""
    # Create a student
    create_response = client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    student_id = create_response.json()["id"]
    
    # Delete the student
    client.delete(
        f"/api/v1/students/{student_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Get all students without inactive
    response = client.get(
        "/api/v1/students/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert student_id not in [s["id"] for s in response.json()["students"]]
    
    # Get all students with inactive
    response = client.get(
        "/api/v1/students/?include_inactive=true",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert student_id in [s["id"] for s in response.json()["students"]]


def test_search_students_case_insensitive(client, admin_token, sample_student_data):
    """Test that student search is case-insensitive"""
    # Create a student with Arabic name
    client.post(
        "/api/v1/students/",
        json=sample_student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Search with different case
    response = client.get(
        "/api/v1/students/search?name=محمد",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["total"] >= 1

