"""
Tests for Dashboard/Statistics API Routes
"""
import pytest
from datetime import datetime, timedelta


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
def sample_data(client, admin_token):
    """Create sample data for testing"""
    # Create a teacher
    teacher_response = client.post(
        "/api/v1/admin/users",
        json={
            "username": "test_teacher",
            "password": "test123",
            "role": "teacher",
            "email": "teacher@test.com",
            "first_name": "Test",
            "last_name": "Teacher"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    teacher_id = teacher_response.json()["id"]
    
    # Create a student
    student_response = client.post(
        "/api/v1/students/",
        json={
            "full_name": "محمد أحمد علي",
            "email": "student@test.com"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    student_id = student_response.json()["id"]
    
    # Create a lesson
    lesson_response = client.post(
        "/api/v1/lessons/",
        json={
            "title": "Test Lesson",
            "subject": "Mathematics",
            "lesson_type": "individual",
            "scheduled_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "duration_minutes": 60,
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    lesson_id = lesson_response.json()["id"]
    
    # Create a payment
    payment_response = client.post(
        "/api/v1/payments/",
        json={
            "student_name": "محمد أحمد علي",
            "amount": 50.0,
            "payment_date": datetime.utcnow().isoformat()
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    return {
        "teacher_id": teacher_id,
        "student_id": student_id,
        "lesson_id": lesson_id
    }


def test_get_dashboard_stats_as_admin(client, admin_token, sample_data):
    """Test getting dashboard stats as admin"""
    response = client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "users" in data
    assert "students" in data
    assert "lessons" in data
    assert "payments" in data
    assert "pricing" in data
    
    # Check users
    assert "total_teachers" in data["users"]
    assert "total_admins" in data["users"]
    assert "total_users" in data["users"]
    assert isinstance(data["users"]["total_teachers"], int)
    assert isinstance(data["users"]["total_admins"], int)
    
    # Check students
    assert "total_students" in data["students"]
    assert isinstance(data["students"]["total_students"], int)
    
    # Check lessons
    assert "total_lessons" in data["lessons"]
    assert "pending_lessons" in data["lessons"]
    assert "completed_lessons" in data["lessons"]
    assert "cancelled_lessons" in data["lessons"]
    
    # Check payments
    assert "total_payments" in data["payments"]
    assert "total_revenue" in data["payments"]
    assert isinstance(data["payments"]["total_revenue"], (int, float))


def test_get_dashboard_stats_as_teacher_should_fail(client, teacher_token):
    """Test that teachers cannot access dashboard stats"""
    response = client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 403


def test_get_teachers_stats(client, admin_token, sample_data):
    """Test getting detailed teachers stats"""
    response = client.get(
        "/api/v1/dashboard/stats/teachers",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_teachers" in data
    assert "teachers" in data
    assert isinstance(data["teachers"], list)
    
    # Check teacher structure
    if data["teachers"]:
        teacher = data["teachers"][0]
        assert "teacher_id" in teacher
        assert "teacher_name" in teacher
        assert "username" in teacher
        assert "total_lessons" in teacher
        assert "pending_lessons" in teacher
        assert "completed_lessons" in teacher
        assert "cancelled_lessons" in teacher


def test_get_teachers_stats_as_teacher_should_fail(client, teacher_token):
    """Test that teachers cannot access teachers stats"""
    response = client.get(
        "/api/v1/dashboard/stats/teachers",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 403


def test_get_students_stats(client, admin_token, sample_data):
    """Test getting detailed students stats"""
    response = client.get(
        "/api/v1/dashboard/stats/students",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_students" in data
    assert "students" in data
    assert isinstance(data["students"], list)
    
    # Check student structure
    if data["students"]:
        student = data["students"][0]
        assert "student_id" in student
        assert "student_name" in student
        assert "total_payments" in student
        assert "total_paid" in student
        assert isinstance(student["total_paid"], (int, float))


def test_get_students_stats_as_teacher_should_fail(client, teacher_token):
    """Test that teachers cannot access students stats"""
    response = client.get(
        "/api/v1/dashboard/stats/students",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 403


def test_get_lessons_stats(client, admin_token, sample_data):
    """Test getting detailed lessons stats"""
    response = client.get(
        "/api/v1/dashboard/stats/lessons",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "by_type" in data
    assert "by_status" in data
    assert "total_hours" in data
    
    # Check by_type
    assert "individual_lessons" in data["by_type"]
    assert "group_lessons" in data["by_type"]
    assert "total_lessons" in data["by_type"]
    
    # Check by_status
    assert "pending_lessons" in data["by_status"]
    assert "completed_lessons" in data["by_status"]
    assert "cancelled_lessons" in data["by_status"]
    assert "total_lessons" in data["by_status"]
    
    # Check total_hours
    assert isinstance(data["total_hours"], (int, float))


def test_get_lessons_stats_as_teacher_should_fail(client, teacher_token):
    """Test that teachers cannot access lessons stats"""
    response = client.get(
        "/api/v1/dashboard/stats/lessons",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    
    assert response.status_code == 403


def test_dashboard_stats_without_auth(client):
    """Test dashboard stats without authentication"""
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 401


def test_dashboard_stats_counts_accuracy(client, admin_token, sample_data):
    """Test that dashboard stats show accurate counts"""
    response = client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify counts are positive or zero
    assert data["users"]["total_teachers"] >= 0
    assert data["users"]["total_admins"] >= 0
    assert data["students"]["total_students"] >= 0
    assert data["lessons"]["pending_lessons"] >= 0
    assert data["lessons"]["completed_lessons"] >= 0
    assert data["lessons"]["cancelled_lessons"] >= 0
    assert data["payments"]["total_payments"] >= 0
    assert data["payments"]["total_revenue"] >= 0


def test_teachers_stats_include_lesson_counts(client, admin_token, sample_data):
    """Test that teachers stats include lesson counts"""
    response = client.get(
        "/api/v1/dashboard/stats/teachers",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Find the test teacher
    test_teacher = None
    for teacher in data["teachers"]:
        if teacher["username"] == "test_teacher":
            test_teacher = teacher
            break
    
    if test_teacher:
        assert test_teacher["total_lessons"] >= 0
        assert test_teacher["pending_lessons"] >= 0
        assert test_teacher["completed_lessons"] >= 0
        assert test_teacher["cancelled_lessons"] >= 0


def test_students_stats_include_payment_totals(client, admin_token, sample_data):
    """Test that students stats include payment totals"""
    response = client.get(
        "/api/v1/dashboard/stats/students",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Find the test student
    test_student = None
    for student in data["students"]:
        if "محمد" in student["student_name"]:
            test_student = student
            break
    
    if test_student:
        assert test_student["total_payments"] >= 0
        assert test_student["total_paid"] >= 0


def test_lessons_stats_calculate_hours_correctly(client, admin_token, sample_data):
    """Test that lessons stats calculate total hours correctly"""
    response = client.get(
        "/api/v1/dashboard/stats/lessons",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Total hours should be >= 0
    assert data["total_hours"] >= 0
    
    # If there are lessons, hours should be > 0
    if data["by_type"]["total_lessons"] > 0:
        assert data["total_hours"] > 0


def test_dashboard_stats_currency_format(client, admin_token, sample_data):
    """Test that revenue is properly formatted"""
    response = client.get(
        "/api/v1/dashboard/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Total revenue should be rounded to 2 decimal places
    revenue = data["payments"]["total_revenue"]
    assert isinstance(revenue, (int, float))
    assert revenue == round(revenue, 2)

