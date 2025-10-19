# Complete API Reference

**General Institute System Backend API**

Base URL: `http://localhost:8000/api/v1`

---

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Student Management](#student-management)
4. [Lesson Management](#lesson-management)
5. [Payment Management](#payment-management)
6. [Pricing Management](#pricing-management)
7. [Admin Management](#admin-management)
8. [Dashboard & Statistics](#dashboard--statistics)
9. [Weekly Reports](#weekly-reports)
10. [Pricing Population](#pricing-population)
11. [Test Endpoints](#test-endpoints)

---

## Authentication

All endpoints (except public ones) require Bearer token authentication:

```
Authorization: Bearer <your-token>
```

### Login

**Endpoint:** `POST /user/login`

**Request:**
```json
{
  "username": "mhmdd400",
  "password": "mhmdd400"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-id-123",
    "username": "mhmdd400",
    "role": "admin",
    "status": "active",
    "last_login": "2025-01-19T10:00:00"
  }
}
```

### Logout

**Endpoint:** `POST /user/logout`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## User Management

### Get Current User Profile

**Endpoint:** `GET /user/profile`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "id": "user-id-123",
  "username": "teacher1",
  "role": "teacher",
  "status": "active",
  "email": "teacher@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": null
}
```

### Update Profile

**Endpoint:** `PUT /user/profile`

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "email": "newemail@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+9876543210"
}
```

**Response (200 OK):**
```json
{
  "id": "user-id-123",
  "username": "teacher1",
  "role": "teacher",
  "status": "active",
  "email": "newemail@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+9876543210",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-19T10:00:00"
}
```

### Change Password

**Endpoint:** `POST /user/change-password`

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "new_password": "newSecurePassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

---

## Student Management

### Create Student (Admin Only)

**Endpoint:** `POST /students/`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "full_name": "محمد أحمد علي",
  "email": "mohammed@example.com",
  "phone": "+1234567890",
  "birthdate": "2010-05-15T00:00:00",
  "notes": "Good student"
}
```

**Response (201 Created):**
```json
{
  "id": "student-id-123",
  "full_name": "محمد أحمد علي",
  "email": "mohammed@example.com",
  "phone": "+1234567890",
  "birthdate": "2010-05-15T00:00:00",
  "notes": "Good student",
  "is_active": true,
  "created_at": "2025-01-19T10:00:00",
  "updated_at": null
}
```

### Get All Students

**Endpoint:** `GET /students/`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `include_inactive` (optional): `true` or `false`

**Response (200 OK):**
```json
{
  "total": 25,
  "students": [
    {
      "id": "student-id-123",
      "full_name": "محمد أحمد علي",
      "email": "mohammed@example.com",
      "phone": "+1234567890",
      "birthdate": "2010-05-15T00:00:00",
      "notes": "Good student",
      "is_active": true,
      "created_at": "2025-01-19T10:00:00",
      "updated_at": null
    }
  ]
}
```

### Search Students

**Endpoint:** `GET /students/search?name=محمد`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `name` (required): Search term

**Response (200 OK):**
```json
{
  "total": 3,
  "students": [
    {
      "id": "student-id-123",
      "full_name": "محمد أحمد علي",
      "email": "mohammed@example.com",
      "is_active": true
    }
  ]
}
```

### Get Student by ID

**Endpoint:** `GET /students/{student_id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "id": "student-id-123",
  "full_name": "محمد أحمد علي",
  "email": "mohammed@example.com",
  "phone": "+1234567890",
  "birthdate": "2010-05-15T00:00:00",
  "notes": "Good student",
  "is_active": true,
  "created_at": "2025-01-19T10:00:00",
  "updated_at": null
}
```

### Update Student (Admin Only)

**Endpoint:** `PUT /students/{student_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "full_name": "أحمد محمد علي",
  "phone": "+9876543210"
}
```

**Response (200 OK):**
```json
{
  "id": "student-id-123",
  "full_name": "أحمد محمد علي",
  "email": "mohammed@example.com",
  "phone": "+9876543210",
  "is_active": true,
  "updated_at": "2025-01-19T10:30:00"
}
```

### Delete Student (Admin Only)

**Endpoint:** `DELETE /students/{student_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (204 No Content)**

---

## Lesson Management

### Create Lesson (Teacher)

**Endpoint:** `POST /lessons/`

**Headers:** `Authorization: Bearer <teacher-token>`

**Request:**
```json
{
  "title": "Algebra Basics",
  "subject": "Mathematics",
  "description": "Introduction to algebra",
  "lesson_type": "individual",
  "scheduled_date": "2025-01-20T14:00:00",
  "duration_minutes": 60,
  "max_students": 1,
  "students": [
    {
      "student_name": "محمد أحمد علي",
      "student_email": "mohammed@example.com"
    }
  ],
  "notes": "Bring calculator",
  "homework": "Complete exercises 1-10"
}
```

**Response (201 Created):**
```json
{
  "id": "lesson-id-123",
  "title": "Algebra Basics",
  "subject": "Mathematics",
  "description": "Introduction to algebra",
  "lesson_type": "individual",
  "scheduled_date": "2025-01-20T14:00:00",
  "duration_minutes": 60,
  "max_students": 1,
  "status": "pending",
  "students": [
    {
      "student_name": "محمد أحمد علي",
      "student_email": "mohammed@example.com"
    }
  ],
  "notes": "Bring calculator",
  "homework": "Complete exercises 1-10",
  "teacher_id": "teacher-id-123",
  "teacher_name": "John Doe",
  "created_at": "2025-01-19T10:00:00",
  "updated_at": null,
  "completed_at": null
}
```

### Get My Lessons (Teacher)

**Endpoint:** `GET /lessons/my-lessons`

**Headers:** `Authorization: Bearer <teacher-token>`

**Query Parameters:**
- `status` (optional): `pending`, `completed`, `cancelled`
- `subject` (optional): Filter by subject

**Response (200 OK):**
```json
{
  "total_lessons": 15,
  "total_hours": 20.5,
  "lessons": [
    {
      "id": "lesson-id-123",
      "title": "Algebra Basics",
      "subject": "Mathematics",
      "lesson_type": "individual",
      "scheduled_date": "2025-01-20T14:00:00",
      "duration_minutes": 60,
      "status": "pending",
      "students": [
        {
          "student_name": "محمد أحمد علي",
          "student_email": "mohammed@example.com"
        }
      ],
      "teacher_id": "teacher-id-123",
      "teacher_name": "John Doe",
      "created_at": "2025-01-19T10:00:00"
    }
  ]
}
```

### Get Lesson by ID

**Endpoint:** `GET /lessons/{lesson_id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "id": "lesson-id-123",
  "title": "Algebra Basics",
  "subject": "Mathematics",
  "lesson_type": "individual",
  "scheduled_date": "2025-01-20T14:00:00",
  "duration_minutes": 60,
  "status": "pending",
  "students": [
    {
      "student_name": "محمد أحمد علي",
      "student_email": "mohammed@example.com"
    }
  ],
  "teacher_id": "teacher-id-123",
  "teacher_name": "John Doe",
  "created_at": "2025-01-19T10:00:00"
}
```

### Update Lesson

**Endpoint:** `PUT /lessons/{lesson_id}`

**Headers:** `Authorization: Bearer <teacher-token>`

**Request:**
```json
{
  "title": "Advanced Algebra",
  "duration_minutes": 90,
  "notes": "Updated notes"
}
```

**Response (200 OK):**
```json
{
  "id": "lesson-id-123",
  "title": "Advanced Algebra",
  "subject": "Mathematics",
  "lesson_type": "individual",
  "scheduled_date": "2025-01-20T14:00:00",
  "duration_minutes": 90,
  "status": "pending",
  "notes": "Updated notes",
  "teacher_name": "John Doe",
  "updated_at": "2025-01-19T10:30:00"
}
```

### Mark Lesson as Completed

**Endpoint:** `POST /lessons/{lesson_id}/complete`

**Headers:** `Authorization: Bearer <teacher-token>`

**Response (200 OK):**
```json
{
  "id": "lesson-id-123",
  "status": "completed",
  "completed_at": "2025-01-19T15:00:00",
  "message": "Lesson marked as completed"
}
```

### Cancel Lesson

**Endpoint:** `POST /lessons/{lesson_id}/cancel`

**Headers:** `Authorization: Bearer <teacher-token>`

**Response (200 OK):**
```json
{
  "id": "lesson-id-123",
  "status": "cancelled",
  "message": "Lesson cancelled"
}
```

---

## Payment Management

### Add Payment (Admin Only)

**Endpoint:** `POST /payments/`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "student_name": "محمد أحمد علي",
  "student_email": "mohammed@example.com",
  "amount": 50.0,
  "payment_date": "2025-01-19T10:00:00",
  "lesson_id": "lesson-id-123",
  "notes": "Payment for Math lessons"
}
```

**Response (201 Created):**
```json
{
  "id": "payment-id-123",
  "student_name": "محمد أحمد علي",
  "student_email": "mohammed@example.com",
  "amount": 50.0,
  "payment_date": "2025-01-19T10:00:00",
  "lesson_id": "lesson-id-123",
  "notes": "Payment for Math lessons",
  "created_at": "2025-01-19T10:00:00"
}
```

### Get Monthly Payments (Admin Only)

**Endpoint:** `GET /payments/?month=1&year=2025`

**Headers:** `Authorization: Bearer <admin-token>`

**Query Parameters:**
- `month` (required): 1-12
- `year` (required): 2000-2100
- `student_name` (optional): Filter by student

**Response (200 OK):**
```json
{
  "month": 1,
  "year": 2025,
  "total_payments": 10,
  "total_amount": 500.0,
  "payments": [
    {
      "id": "payment-id-123",
      "student_name": "محمد أحمد علي",
      "amount": 50.0,
      "payment_date": "2025-01-15T10:00:00",
      "notes": "Payment for Math"
    }
  ]
}
```

### Get Student Payments (Admin Only)

**Endpoint:** `GET /payments/student/{student_name}`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "student_name": "محمد أحمد علي",
  "total_payments": 5,
  "total_amount": 250.0,
  "payments": [
    {
      "id": "payment-id-123",
      "student_name": "محمد أحمد علي",
      "amount": 50.0,
      "payment_date": "2025-01-15T10:00:00",
      "notes": "Payment for Math"
    }
  ]
}
```

### Get Student Total (Admin Only)

**Endpoint:** `GET /payments/student/{student_name}/total`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "student_name": "محمد أحمد علي",
  "total_payments": 5,
  "total_amount": 250.0,
  "currency": "USD"
}
```

### Delete Payment (Admin Only)

**Endpoint:** `DELETE /payments/{payment_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (204 No Content)**

---

## Pricing Management

### Create Pricing (Admin Only)

**Endpoint:** `POST /pricing/`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "subject": "Mathematics",
  "individual_price": 50.0,
  "group_price": 30.0,
  "currency": "USD"
}
```

**Response (201 Created):**
```json
{
  "id": "pricing-id-123",
  "subject": "Mathematics",
  "individual_price": 50.0,
  "group_price": 30.0,
  "currency": "USD",
  "is_active": true,
  "created_at": "2025-01-19T10:00:00",
  "updated_at": null
}
```

### Get All Pricing (Admin Only)

**Endpoint:** `GET /pricing/`

**Headers:** `Authorization: Bearer <admin-token>`

**Query Parameters:**
- `include_inactive` (optional): `true` or `false`

**Response (200 OK):**
```json
{
  "total": 15,
  "pricing": [
    {
      "id": "pricing-id-123",
      "subject": "Mathematics",
      "individual_price": 50.0,
      "group_price": 30.0,
      "currency": "USD",
      "is_active": true,
      "created_at": "2025-01-19T10:00:00"
    }
  ]
}
```

### Lookup Price (Public)

**Endpoint:** `GET /pricing/lookup/{subject}?lesson_type=individual`

**Headers:** `Authorization: Bearer <token>` (optional)

**Query Parameters:**
- `lesson_type` (required): `individual` or `group`

**Response (200 OK):**
```json
{
  "subject": "Mathematics",
  "lesson_type": "individual",
  "price_per_hour": 50.0,
  "currency": "USD",
  "found": true
}
```

### Get Public Pricing

**Endpoint:** `GET /pricing/public/all`

**No Authentication Required**

**Response (200 OK):**
```json
[
  {
    "id": "pricing-id-123",
    "subject": "Mathematics",
    "individual_price": 50.0,
    "group_price": 30.0,
    "currency": "USD",
    "is_active": true
  }
]
```

### Update Pricing (Admin Only)

**Endpoint:** `PUT /pricing/{pricing_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "individual_price": 55.0,
  "group_price": 35.0
}
```

**Response (200 OK):**
```json
{
  "id": "pricing-id-123",
  "subject": "Mathematics",
  "individual_price": 55.0,
  "group_price": 35.0,
  "currency": "USD",
  "is_active": true,
  "updated_at": "2025-01-19T10:30:00"
}
```

### Delete Pricing (Admin Only)

**Endpoint:** `DELETE /pricing/{pricing_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (204 No Content)**

---

## Admin Management

### Create User (Admin Only)

**Endpoint:** `POST /admin/users`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "username": "newteacher",
  "password": "secure123",
  "role": "teacher",
  "email": "teacher@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response (201 Created):**
```json
{
  "id": "user-id-123",
  "username": "newteacher",
  "role": "teacher",
  "status": "active",
  "email": "teacher@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1234567890",
  "created_at": "2025-01-19T10:00:00"
}
```

### Get All Users (Admin Only)

**Endpoint:** `GET /admin/users`

**Headers:** `Authorization: Bearer <admin-token>`

**Query Parameters:**
- `role` (optional): `admin` or `teacher`
- `status` (optional): `active` or `inactive`

**Response (200 OK):**
```json
{
  "total": 10,
  "users": [
    {
      "id": "user-id-123",
      "username": "teacher1",
      "role": "teacher",
      "status": "active",
      "email": "teacher@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

### Update User (Admin Only)

**Endpoint:** `PUT /admin/users/{user_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
{
  "email": "newemail@example.com",
  "status": "active"
}
```

**Response (200 OK):**
```json
{
  "id": "user-id-123",
  "username": "teacher1",
  "role": "teacher",
  "status": "active",
  "email": "newemail@example.com",
  "updated_at": "2025-01-19T10:30:00"
}
```

### Delete User (Admin Only)

**Endpoint:** `DELETE /admin/users/{user_id}`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (204 No Content)**

---

## Dashboard & Statistics

### Get Dashboard Stats (Admin Only)

**Endpoint:** `GET /dashboard/stats`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "users": {
    "total_teachers": 5,
    "total_admins": 2,
    "total_users": 7
  },
  "students": {
    "total_students": 25
  },
  "lessons": {
    "total_lessons": 100,
    "pending_lessons": 30,
    "completed_lessons": 65,
    "cancelled_lessons": 5
  },
  "payments": {
    "total_payments": 50,
    "total_revenue": 2500.00
  },
  "pricing": {
    "active_subjects": 15
  }
}
```

### Get Teachers Stats (Admin Only)

**Endpoint:** `GET /dashboard/stats/teachers`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "total_teachers": 5,
  "teachers": [
    {
      "teacher_id": "teacher-id-123",
      "teacher_name": "محمد أحمد",
      "username": "teacher1",
      "email": "teacher@example.com",
      "total_lessons": 20,
      "pending_lessons": 5,
      "completed_lessons": 14,
      "cancelled_lessons": 1
    }
  ]
}
```

### Get Students Stats (Admin Only)

**Endpoint:** `GET /dashboard/stats/students`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "total_students": 25,
  "students": [
    {
      "student_id": "student-id-123",
      "student_name": "محمد أحمد علي",
      "email": "mohammed@example.com",
      "phone": "+1234567890",
      "total_payments": 3,
      "total_paid": 150.00
    }
  ]
}
```

### Get Lessons Stats (Admin Only)

**Endpoint:** `GET /dashboard/stats/lessons`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "by_type": {
    "individual_lessons": 60,
    "group_lessons": 40,
    "total_lessons": 100
  },
  "by_status": {
    "pending_lessons": 30,
    "completed_lessons": 65,
    "cancelled_lessons": 5,
    "total_lessons": 100
  },
  "total_hours": 500.50
}
```

---

## Weekly Reports

### Send Weekly Report (Admin Only)

**Endpoint:** `POST /weekly-report/send-weekly-report`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Weekly lesson report sent successfully",
  "recipient": "EMAIL_TO configured in .env",
  "triggered_by": "admin@example.com"
}
```

**Note:** This endpoint sends a CSV report of all lessons from the past 7 days to the configured `EMAIL_TO` address.

---

## Pricing Population

### Populate Default Pricing (Admin Only)

**Endpoint:** `POST /populate-pricing/populate-defaults`

**Headers:** `Authorization: Bearer <admin-token>`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Pricing population completed",
  "created": 15,
  "skipped": 0,
  "total_subjects": 15,
  "errors": null,
  "triggered_by": "admin@example.com"
}
```

**Note:** Populates database with 15 default subjects (Mathematics, Physics, Chemistry, Biology, English, History, Geography, Computer Science, Programming, Arabic, French, Spanish, Music, Art, Physical Education).

### Populate Custom Pricing (Admin Only)

**Endpoint:** `POST /populate-pricing/populate-custom`

**Headers:** `Authorization: Bearer <admin-token>`

**Request:**
```json
[
  {
    "subject": "Psychology",
    "individual_price": 55.0,
    "group_price": 35.0,
    "currency": "USD"
  },
  {
    "subject": "Economics",
    "individual_price": 60.0,
    "group_price": 40.0,
    "currency": "USD"
  }
]
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Custom pricing population completed",
  "created": 2,
  "skipped": 0,
  "total_subjects": 2,
  "errors": null,
  "triggered_by": "admin@example.com"
}
```

### Get Default Subjects (Public)

**Endpoint:** `GET /populate-pricing/default-subjects`

**No Authentication Required**

**Response (200 OK):**
```json
{
  "subjects": [
    {
      "subject": "Mathematics",
      "individual_price": 50.0,
      "group_price": 30.0,
      "currency": "USD"
    }
  ],
  "total": 15,
  "note": "These are the default subjects that can be populated using /populate-defaults endpoint"
}
```

---

## Test Endpoints (Development Only)

### Test Email

**Endpoint:** `POST /email-test/send-test`

**Headers:** `Authorization: Bearer <admin-token>` (Optional in dev)

**Request:**
```json
{
  "to_email": "recipient@example.com",
  "subject": "Test Email",
  "body": "This is a test message!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Email sent successfully to recipient@example.com",
  "from": "your-email@gmail.com",
  "to": "recipient@example.com",
  "subject": "Test Email"
}
```

### Test Crash

**Endpoint:** `GET /test-crash/test-crash`

**No Authentication Required (Dev only)**

**Response (500 Internal Server Error):**
```json
{
  "detail": "Internal server error. The issue has been logged and reported."
}
```

**Note:** This endpoint triggers a test crash to verify email notifications are working.

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error. The issue has been logged and reported."
}
```

---

## Status Codes Summary

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server error |

---

## Notes

1. **Authentication:** Most endpoints require a valid Bearer token. Get one by logging in at `/user/login`.

2. **Admin vs Teacher:** Some endpoints are admin-only, others are available to both admins and teachers.

3. **Arabic Names:** The system fully supports Arabic names for students and teachers.

4. **Email Notifications:** Crash notifications are automatically sent to `EMAIL_TO` when errors occur.

5. **Weekly Reports:** Automatic weekly lesson reports are sent every Saturday at 9:00 AM.

6. **Development Mode:** Test endpoints are only available when `DEBUG=True` or `ENVIRONMENT=development`.

---

**Last Updated:** January 19, 2025

**API Version:** 1.0.0

