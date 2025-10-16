# Lessons API Documentation

## Overview
Lesson submission and management endpoints for teachers.

---

## Endpoints

### 1. Submit Lesson
**POST** `/api/v1/lessons/submit`

**Access:** Teacher only

**Description:** Submit a new lesson record.

**Request Body:**
```json
{
  "subject": "Math",
  "lesson_type": "individual",
  "duration_minutes": 60,
  "scheduled_date": "2024-01-20T14:00:00Z",
  "students": [
    {
      "name": "Ahmad Ali",
      "grade": "Grade 10"
    }
  ],
  "notes": "Covered algebra basics"
}
```

**Response (201):**
```json
{
  "id": "lesson-uuid",
  "teacher_id": "teacher-uuid",
  "teacher_name": "John Doe",
  "subject": "Math",
  "lesson_type": "individual",
  "duration_minutes": 60,
  "scheduled_date": "2024-01-20T14:00:00Z",
  "status": "pending",
  "students": [
    {
      "name": "Ahmad Ali",
      "grade": "Grade 10"
    }
  ],
  "notes": "Covered algebra basics",
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

### 2. Get My Lessons
**GET** `/api/v1/lessons/my-lessons`

**Access:** Teacher or Admin

**Description:** Get all lessons for the authenticated teacher (or all lessons for admin).

**Query Parameters:**
- `lesson_type` (optional): Filter by type (`individual` or `group`)
- `status` (optional): Filter by status (`pending`, `completed`, `cancelled`)
- `subject` (optional): Filter by subject name

**Example:** `GET /api/v1/lessons/my-lessons?lesson_type=individual&status=completed`

**Response (200):**
```json
{
  "lessons": [
    {
      "id": "lesson-uuid-1",
      "teacher_id": "teacher-uuid",
      "teacher_name": "John Doe",
      "subject": "Math",
      "lesson_type": "individual",
      "duration_minutes": 60,
      "scheduled_date": "2024-01-20T14:00:00Z",
      "status": "completed",
      "students": [
        {
          "name": "Ahmad Ali",
          "grade": "Grade 10"
        }
      ],
      "completed_at": "2024-01-20T15:00:00Z",
      "created_at": "2024-01-20T10:00:00Z"
    }
  ],
  "total_lessons": 1,
  "total_hours": 1.0
}
```

---

### 3. Get Lesson by ID
**GET** `/api/v1/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin (all lessons)

**Description:** Get detailed information about a specific lesson.

**Response (200):**
```json
{
  "id": "lesson-uuid",
  "teacher_id": "teacher-uuid",
  "teacher_name": "John Doe",
  "subject": "Physics",
  "lesson_type": "group",
  "duration_minutes": 90,
  "scheduled_date": "2024-01-21T10:00:00Z",
  "status": "pending",
  "students": [
    {
      "name": "Sara Ahmed",
      "grade": "Grade 11"
    },
    {
      "name": "Omar Hassan",
      "grade": "Grade 11"
    }
  ],
  "notes": "Introduction to mechanics",
  "created_at": "2024-01-20T12:00:00Z",
  "updated_at": "2024-01-20T12:00:00Z"
}
```

---

### 4. Update Lesson
**PUT** `/api/v1/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin

**Description:** Update lesson details. Can only update pending lessons.

**Request Body:**
```json
{
  "subject": "Physics",
  "duration_minutes": 90,
  "scheduled_date": "2024-01-21T11:00:00Z",
  "notes": "Updated notes",
  "status": "completed"
}
```

**Response (200):**
```json
{
  "id": "lesson-uuid",
  "teacher_id": "teacher-uuid",
  "teacher_name": "John Doe",
  "subject": "Physics",
  "lesson_type": "individual",
  "duration_minutes": 90,
  "scheduled_date": "2024-01-21T11:00:00Z",
  "status": "completed",
  "students": [
    {
      "name": "Ahmad Ali",
      "grade": "Grade 10"
    }
  ],
  "notes": "Updated notes",
  "completed_at": "2024-01-21T12:00:00Z",
  "updated_at": "2024-01-21T12:00:00Z"
}
```

---

### 5. Delete Lesson (Cancel)
**DELETE** `/api/v1/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin

**Description:** Cancel a lesson (soft delete - sets status to cancelled).

**Response (200):**
```json
{
  "message": "Lesson cancelled successfully"
}
```

---

### 6. Get Lessons Summary
**GET** `/api/v1/lessons/summary`

**Access:** Teacher or Admin

**Description:** Get aggregated statistics grouped by subject and lesson type.

**Response (200):**
```json
{
  "summary": [
    {
      "subject": "Math",
      "lesson_type": "individual",
      "total_lessons": 12,
      "total_hours": 18.0,
      "completed_lessons": 10,
      "pending_lessons": 2,
      "cancelled_lessons": 0
    },
    {
      "subject": "Physics",
      "lesson_type": "group",
      "total_lessons": 8,
      "total_hours": 12.0,
      "completed_lessons": 6,
      "pending_lessons": 2,
      "cancelled_lessons": 0
    }
  ],
  "overall_total": 20,
  "overall_hours": 30.0
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Cannot update completed lesson"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to access this lesson"
}
```

### 404 Not Found
```json
{
  "detail": "Lesson not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "duration_minutes"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

