"""
Comprehensive tests for Lesson routes/endpoints
Tests: Submit lesson, get lessons, update, delete
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime
from app.models.user import User, UserRole, UserStatus
from app.models.lesson import Lesson, LessonType, LessonStatus
from app.core.security import get_password_hash, create_access_token


class TestSubmitLessonEndpoint:
    """Test POST /api/v1/lessons/submit - Teacher submits lesson"""
    
    def test_teacher_submits_individual_lesson_successfully(self, client, mock_db):
        """Test teacher can submit individual lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            first_name="John",
            last_name="Teacher"
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "Math Basics",
                    "subject": "Mathematics",
                    "lesson_type": "individual",
                    "scheduled_date": "2024-01-15T10:00:00",
                    "duration_minutes": 60,
                    "students": [
                        {"student_name": "Student A", "student_email": "a@example.com"}
                    ]
                }
            )
            
            assert response.status_code == 201
            data = response.json()
            
            assert data["title"] == "Math Basics"
            assert data["subject"] == "Mathematics"
            assert data["lesson_type"] == "individual"
            assert data["teacher_name"] == "John Teacher"
            assert data["status"] == "pending"  # Starts as pending
            assert len(data["students"]) == 1
            
            # Verify saved in database
            lesson_doc = mock_db["lessons"].find_one({"title": "Math Basics"})
            assert lesson_doc is not None
    
    def test_teacher_submits_group_lesson_successfully(self, client, mock_db):
        """Test teacher can submit group lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            first_name="Jane",
            last_name="Doe"
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "Group Physics",
                    "subject": "Physics",
                    "lesson_type": "group",
                    "scheduled_date": "2024-02-20T14:00:00",
                    "duration_minutes": 90,
                    "max_students": 10,
                    "students": [
                        {"student_name": "S1"},
                        {"student_name": "S2"},
                        {"student_name": "S3"}
                    ]
                }
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["lesson_type"] == "group"
            assert data["max_students"] == 10
            assert len(data["students"]) == 3
    
    def test_submit_lesson_uses_teacher_full_name(self, client, mock_db):
        """Test lesson uses teacher's full name"""
        teacher = User(
            username="jdoe",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            first_name="John",
            last_name="Doe"
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "Test",
                    "subject": "Math",
                    "lesson_type": "individual",
                    "scheduled_date": "2024-01-15T10:00:00",
                    "duration_minutes": 60
                }
            )
            
            assert response.status_code == 201
            assert response.json()["teacher_name"] == "John Doe"
    
    def test_submit_lesson_without_required_fields_fails(self, client, mock_db):
        """Test submitting lesson without required fields fails"""
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
            
            # Missing title
            response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "subject": "Math",
                    "lesson_type": "individual",
                    "scheduled_date": "2024-01-15T10:00:00",
                    "duration_minutes": 60
                }
            )
            assert response.status_code == 422
    
    def test_admin_cannot_submit_lesson(self, client, mock_db):
        """Test admin cannot submit lessons (only teachers)"""
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
        
        with patch('app.api.deps.mongo_db') as mock_deps:
            mock_deps.users_collection = mock_db["users"]
            
            response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "Test",
                    "subject": "Math",
                    "lesson_type": "individual",
                    "scheduled_date": "2024-01-15T10:00:00",
                    "duration_minutes": 60
                }
            )
            
            assert response.status_code == 403
            assert "Teacher access required" in response.json()["detail"]


class TestGetMyLessonsEndpoint:
    """Test GET /api/v1/lessons/my-lessons - Get teacher's lessons"""
    
    def test_teacher_gets_own_lessons(self, client, mock_db):
        """Test teacher can retrieve their own lessons"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        # Create lessons for teacher
        lesson1 = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Lesson 1",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 10),
            duration_minutes=60
        )
        lesson2 = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Lesson 2",
            subject="Physics",
            lesson_type=LessonType.GROUP,
            scheduled_date=datetime(2024, 1, 15),
            duration_minutes=90
        )
        
        mock_db["lessons"].insert_one(lesson1.to_dict())
        mock_db["lessons"].insert_one(lesson2.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/lessons/my-lessons",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["total_lessons"] == 2
            assert data["total_hours"] == 2.5  # 60 + 90 = 150 min = 2.5 hours
            assert len(data["lessons"]) == 2
    
    def test_teacher_filters_lessons_by_type(self, client, mock_db):
        """Test filtering lessons by type (individual/group)"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        # Create mixed lessons
        individual = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Individual",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        group = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Group",
            subject="Physics",
            lesson_type=LessonType.GROUP,
            scheduled_date=datetime(2024, 1, 2),
            duration_minutes=60
        )
        
        mock_db["lessons"].insert_one(individual.to_dict())
        mock_db["lessons"].insert_one(group.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            # Filter by individual
            response = client.get(
                "/api/v1/lessons/my-lessons?lesson_type=individual",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_lessons"] == 1
            assert data["lessons"][0]["lesson_type"] == "individual"
    
    def test_teacher_filters_lessons_by_status(self, client, mock_db):
        """Test filtering lessons by status"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        # Create lessons with different statuses
        pending = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Pending",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.PENDING
        )
        completed = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Completed",
            subject="Physics",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 2),
            duration_minutes=60,
            status=LessonStatus.COMPLETED
        )
        
        mock_db["lessons"].insert_one(pending.to_dict())
        mock_db["lessons"].insert_one(completed.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            # Filter by completed
            response = client.get(
                "/api/v1/lessons/my-lessons?lesson_status=completed",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_lessons"] == 1
            assert data["lessons"][0]["status"] == "completed"
    
    def test_teacher_only_sees_own_lessons(self, client, mock_db):
        """Test teacher only sees their own lessons, not others"""
        teacher1 = User(
            username="teacher1",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        teacher2 = User(
            username="teacher2",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher1.to_dict())
        mock_db["users"].insert_one(teacher2.to_dict())
        
        # Create lessons for both teachers
        lesson1 = Lesson(
            teacher_id=teacher1._id,
            teacher_name="Teacher 1",
            title="T1 Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        lesson2 = Lesson(
            teacher_id=teacher2._id,
            teacher_name="Teacher 2",
            title="T2 Lesson",
            subject="Physics",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 2),
            duration_minutes=60
        )
        
        mock_db["lessons"].insert_one(lesson1.to_dict())
        mock_db["lessons"].insert_one(lesson2.to_dict())
        
        # Teacher 1 token
        token = create_access_token({
            "sub": teacher1._id,
            "username": teacher1.username,
            "role": teacher1.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/lessons/my-lessons",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Should only see own lesson
            assert data["total_lessons"] == 1
            assert data["lessons"][0]["title"] == "T1 Lesson"


class TestUpdateLessonEndpoint:
    """Test PUT /api/v1/lessons/update-lesson/{lesson_id} - Update lesson"""
    
    def test_teacher_updates_own_lesson_successfully(self, client, mock_db):
        """Test teacher can update their own pending lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Old Title",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.PENDING
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "New Title",
                    "notes": "Updated notes"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "New Title"
            assert data["notes"] == "Updated notes"
    
    def test_teacher_cannot_update_completed_lesson(self, client, mock_db):
        """Test teacher cannot update completed lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Completed Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.COMPLETED
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"title": "New Title"}
            )
            
            assert response.status_code == 400
            assert "Cannot update completed lesson" in response.json()["detail"]
    
    def test_teacher_cannot_update_other_teacher_lesson(self, client, mock_db):
        """Test teacher cannot update another teacher's lesson"""
        teacher1 = User(
            username="teacher1",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        teacher2 = User(
            username="teacher2",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher1.to_dict())
        mock_db["users"].insert_one(teacher2.to_dict())
        
        # Lesson belongs to teacher2
        lesson = Lesson(
            teacher_id=teacher2._id,
            teacher_name="Teacher 2",
            title="T2 Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        # Teacher 1 tries to update
        token = create_access_token({
            "sub": teacher1._id,
            "username": teacher1.username,
            "role": teacher1.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"title": "Hacked"}
            )
            
            assert response.status_code == 403
            assert "Not authorized" in response.json()["detail"]
    
    def test_mark_lesson_as_completed(self, client, mock_db):
        """Test teacher can mark lesson as completed"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="To Complete",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.PENDING
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "completed"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "completed"
            assert data["completed_at"] is not None


class TestDeleteLessonEndpoint:
    """Test DELETE /api/v1/lessons/delete-lesson/{lesson_id} - Delete lesson"""
    
    def test_teacher_deletes_own_pending_lesson(self, client, mock_db):
        """Test teacher can delete (cancel) their own pending lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="To Delete",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.PENDING
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.delete(
                f"/api/v1/lessons/delete-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            assert "cancelled successfully" in response.json()["message"]
            
            # Verify lesson still exists but is cancelled (soft delete)
            deleted = mock_db["lessons"].find_one({"_id": lesson._id})
            assert deleted is not None
            assert deleted["status"] == "cancelled"
    
    def test_teacher_cannot_delete_completed_lesson(self, client, mock_db):
        """Test teacher cannot delete completed lesson"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Completed",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            status=LessonStatus.COMPLETED
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.delete(
                f"/api/v1/lessons/delete-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 400
            assert "Cannot delete completed lesson" in response.json()["detail"]
    
    def test_soft_delete_preserves_lesson_data(self, client, mock_db):
        """Test soft delete preserves all lesson information"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Preserve",
            description="Important lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60,
            students=[{"student_name": "Student"}],
            notes="Important notes",
            homework="Chapter 1"
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.delete(
                f"/api/v1/lessons/delete-lesson/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            
            # Verify data preserved
            preserved = mock_db["lessons"].find_one({"_id": lesson._id})
            assert preserved["title"] == "Preserve"
            assert preserved["description"] == "Important lesson"
            assert preserved["notes"] == "Important notes"
            assert preserved["homework"] == "Chapter 1"
            assert len(preserved["students"]) == 1


class TestGetLessonByIdEndpoint:
    """Test GET /api/v1/lessons/{lesson_id} - Get lesson by ID"""
    
    def test_teacher_gets_own_lesson_by_id(self, client, mock_db):
        """Test teacher can get their own lesson by ID"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="My Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                f"/api/v1/lessons/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "My Lesson"
    
    def test_teacher_cannot_get_other_teacher_lesson(self, client, mock_db):
        """Test teacher cannot access another teacher's lesson"""
        teacher1 = User(
            username="teacher1",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        teacher2 = User(
            username="teacher2",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(teacher1.to_dict())
        mock_db["users"].insert_one(teacher2.to_dict())
        
        # Lesson belongs to teacher2
        lesson = Lesson(
            teacher_id=teacher2._id,
            teacher_name="Teacher 2",
            title="T2 Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        # Teacher 1 tries to access
        token = create_access_token({
            "sub": teacher1._id,
            "username": teacher1.username,
            "role": teacher1.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                f"/api/v1/lessons/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 403
            assert "Not authorized" in response.json()["detail"]
    
    def test_admin_can_get_any_lesson(self, client, mock_db):
        """Test admin can access any teacher's lesson"""
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("pass123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE
        )
        mock_db["users"].insert_one(admin.to_dict())
        mock_db["users"].insert_one(teacher.to_dict())
        
        lesson = Lesson(
            teacher_id=teacher._id,
            teacher_name="Teacher",
            title="Teacher Lesson",
            subject="Math",
            lesson_type=LessonType.INDIVIDUAL,
            scheduled_date=datetime(2024, 1, 1),
            duration_minutes=60
        )
        mock_db["lessons"].insert_one(lesson.to_dict())
        
        # Admin accesses teacher's lesson
        token = create_access_token({
            "sub": admin._id,
            "username": admin.username,
            "role": admin.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                f"/api/v1/lessons/{lesson._id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Teacher Lesson"
    
    def test_get_nonexistent_lesson_returns_404(self, client, mock_db):
        """Test getting non-existent lesson returns 404"""
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
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            response = client.get(
                "/api/v1/lessons/nonexistent-id",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 404
            assert "Lesson not found" in response.json()["detail"]


class TestLessonIntegration:
    """Test complete lesson workflows"""
    
    def test_complete_lesson_lifecycle(self, client, mock_db):
        """Test complete flow: submit → update → mark completed"""
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role=UserRole.TEACHER,
            status=UserStatus.ACTIVE,
            first_name="Test",
            last_name="Teacher"
        )
        mock_db["users"].insert_one(teacher.to_dict())
        
        token = create_access_token({
            "sub": teacher._id,
            "username": teacher.username,
            "role": teacher.role.value
        })
        
        with patch('app.api.v1.endpoints.lessons.mongo_db') as mock_mongo, \
             patch('app.api.deps.mongo_db') as mock_deps:
            mock_mongo.lessons_collection = mock_db["lessons"]
            mock_deps.users_collection = mock_db["users"]
            
            # 1. Submit lesson
            submit_response = client.post(
                "/api/v1/lessons/submit",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": "Lifecycle Test",
                    "subject": "Math",
                    "lesson_type": "individual",
                    "scheduled_date": "2024-01-15T10:00:00",
                    "duration_minutes": 60
                }
            )
            assert submit_response.status_code == 201
            lesson_id = submit_response.json()["id"]
            
            # 2. Get lesson
            get_response = client.get(
                f"/api/v1/lessons/{lesson_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert get_response.status_code == 200
            
            # 3. Update lesson
            update_response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson_id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"notes": "Session went well"}
            )
            assert update_response.status_code == 200
            assert update_response.json()["notes"] == "Session went well"
            
            # 4. Mark as completed
            complete_response = client.put(
                f"/api/v1/lessons/update-lesson/{lesson_id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "completed"}
            )
            assert complete_response.status_code == 200
            assert complete_response.json()["status"] == "completed"

