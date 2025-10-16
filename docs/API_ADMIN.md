# Admin API Documentation

## Overview
Administrative endpoints for user management, earnings reports, and system configuration.

**All endpoints require Admin authentication.**

---

## User Management Endpoints

### 1. Create User
**POST** `/api/v1/admin/users`

**Access:** Admin only

**Description:** Create a new user (teacher or admin) account.

**Request Body:**
```json
{
  "username": "newteacher",
  "email": "teacher@example.com",
  "password": "password123",
  "role": "teacher",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "id": "uuid-here",
  "username": "newteacher",
  "email": "teacher@example.com",
  "role": "teacher",
  "status": "active",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 2. Get All Users
**GET** `/api/v1/admin/users`

**Access:** Admin only

**Description:** Get paginated list of all users with optional filters.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 50, max: 100)
- `role` (optional): Filter by role (`teacher` or `admin`)
- `status` (optional): Filter by status (`active`, `inactive`, `suspended`)

**Example:** `GET /api/v1/admin/users?role=teacher&limit=20`

**Response (200):**
```json
{
  "users": [
    {
      "id": "uuid-1",
      "username": "teacher1",
      "email": "teacher1@example.com",
      "role": "teacher",
      "status": "active",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20
}
```

---

### 3. Get User by ID
**GET** `/api/v1/admin/users/{user_id}`

**Access:** Admin only

**Description:** Get detailed information about a specific user.

**Response (200):**
```json
{
  "id": "uuid-here",
  "username": "teacher1",
  "email": "teacher1@example.com",
  "role": "teacher",
  "status": "active",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:20:00Z"
}
```

---

### 4. Update User
**PUT** `/api/v1/admin/users/{user_id}`

**Access:** Admin only

**Description:** Update user information.

**Request Body:**
```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "email": "newemail@example.com",
  "phone": "+9876543210",
  "status": "active",
  "role": "admin"
}
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "username": "teacher1",
  "email": "newemail@example.com",
  "role": "admin",
  "status": "active",
  "first_name": "Johnny",
  "last_name": "Doe",
  "phone": "+9876543210",
  "updated_at": "2024-01-20T15:00:00Z"
}
```

---

### 5. Deactivate User (Soft Delete)
**DELETE** `/api/v1/admin/users/{user_id}`

**Access:** Admin only

**Description:** Deactivate a user account (soft delete - preserves data).

**Response (200):**
```json
{
  "message": "User deactivated successfully"
}
```

---

### 6. Reset User Password
**POST** `/api/v1/admin/users/{user_id}/reset-password`

**Access:** Admin only

**Description:** Reset a user's password.

**Request Body:**
```json
{
  "new_password": "newpassword123"
}
```

**Response (200):**
```json
{
  "message": "Password reset successfully"
}
```

---

## Earnings & Reports Endpoints

### 7. Get Teacher Earnings
**GET** `/api/v1/admin/teacher-earnings/{teacher_id}`

**Access:** Admin only

**Description:** Get detailed earnings breakdown for a teacher by subject.

**Query Parameters:**
- `month` (optional): Filter by month (1-12)
- `year` (optional): Filter by year

**Example:** `GET /api/v1/admin/teacher-earnings/uuid?month=1&year=2024`

**Response (200):**
```json
{
  "teacher_id": "uuid-here",
  "teacher_name": "John Doe",
  "month": 1,
  "year": 2024,
  "total_lessons": 15,
  "total_hours": 22.5,
  "total_earnings": 562.50,
  "by_subject": [
    {
      "subject": "Math",
      "lesson_type": "individual",
      "lesson_count": 8,
      "total_hours": 12.0,
      "price_per_hour": 25.00,
      "total_amount": 300.00
    },
    {
      "subject": "Physics",
      "lesson_type": "group",
      "lesson_count": 7,
      "total_hours": 10.5,
      "price_per_hour": 25.00,
      "total_amount": 262.50
    }
  ]
}
```

---

### 8. Get Subject Prices
**GET** `/api/v1/admin/subject-prices`

**Access:** Admin only

**Description:** Get all subject pricing information.

**Response (200):**
```json
{
  "prices": [
    {
      "subject": "Math",
      "individual_price": 25.00,
      "group_price": 25.00
    },
    {
      "subject": "Physics",
      "individual_price": 25.00,
      "group_price": 25.00
    }
  ],
  "default_individual_price": 25.00,
  "default_group_price": 25.00
}
```

---

## Error Responses

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 400 Bad Request
```json
{
  "detail": "User is already inactive"
}
```

