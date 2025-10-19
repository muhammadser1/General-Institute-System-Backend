"""
Tests for Dashboard/Statistics API Routes
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash, create_access_token


class TestDashboardStats:
    """Test GET /dashboard/stats"""
    
    def test_get_dashboard_stats_as_admin(self, client, mock_db):
        """Test getting dashboard stats as admin"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.users_collection = mock_db["users"]
            mock_mongo.students_collection = mock_db["students"]
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_mongo.payments_collection = mock_db["payments"]
            mock_mongo.pricing_collection = mock_db["pricing"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "users" in data
            assert "students" in data
            assert "lessons" in data
            assert "payments" in data
            assert "pricing" in data
    
    def test_get_dashboard_stats_as_teacher_should_fail(self, client, mock_db):
        """Test that teachers cannot access dashboard stats"""
        # Create teacher user
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.deps.mongo_db') as mock_deps:
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 403
    
    def test_get_dashboard_stats_without_auth(self, client):
        """Test dashboard stats without authentication"""
        response = client.get("/api/v1/dashboard/stats")
        assert response.status_code in [401, 403]
    
    def test_get_dashboard_stats_with_month_filter(self, client, mock_db):
        """Test getting dashboard stats filtered by month"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.users_collection = mock_db["users"]
            mock_mongo.students_collection = mock_db["students"]
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_mongo.payments_collection = mock_db["payments"]
            mock_mongo.pricing_collection = mock_db["pricing"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats?month=1&year=2025",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "filter" in data
            assert data["filter"]["month"] == 1
            assert data["filter"]["year"] == 2025


class TestTeachersStats:
    """Test GET /dashboard/stats/teachers"""
    
    def test_get_teachers_stats(self, client, mock_db):
        """Test getting detailed teachers stats"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.users_collection = mock_db["users"]
            mock_mongo.lessons_collection = mock_db["lessons"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/teachers",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "total_teachers" in data
            assert "teachers" in data
            assert isinstance(data["teachers"], list)
    
    def test_get_teachers_stats_as_teacher_should_fail(self, client, mock_db):
        """Test that teachers cannot access teachers stats"""
        # Create teacher user
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.deps.mongo_db') as mock_deps:
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/teachers",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 403


class TestStudentsStats:
    """Test GET /dashboard/stats/students"""
    
    def test_get_students_stats(self, client, mock_db):
        """Test getting detailed students stats"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.students_collection = mock_db["students"]
            mock_mongo.payments_collection = mock_db["payments"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/students",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "total_students" in data
            assert "students" in data
            assert isinstance(data["students"], list)
    
    def test_get_students_stats_as_teacher_should_fail(self, client, mock_db):
        """Test that teachers cannot access students stats"""
        # Create teacher user
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.deps.mongo_db') as mock_deps:
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/students",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 403


class TestLessonsStats:
    """Test GET /dashboard/stats/lessons"""
    
    def test_get_lessons_stats(self, client, mock_db):
        """Test getting detailed lessons stats"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/lessons",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "by_type" in data
            assert "by_status" in data
            assert "total_hours" in data
    
    def test_get_lessons_stats_with_month_filter(self, client, mock_db):
        """Test getting lessons stats filtered by month"""
        # Create admin user
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.dashboard.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/lessons?month=1&year=2025",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "filter" in data
            assert data["filter"]["month"] == 1
            assert data["filter"]["year"] == 2025
    
    def test_get_lessons_stats_as_teacher_should_fail(self, client, mock_db):
        """Test that teachers cannot access lessons stats"""
        # Create teacher user
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.deps.mongo_db') as mock_deps:
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/dashboard/stats/lessons",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 403
