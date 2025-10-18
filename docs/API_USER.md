# User API Documentation

## Overview
User authentication and profile management endpoints.

---

## Endpoints

### 1. Teacher Signup
**POST** `/api/v1/user/signup`

**Access:** Public (No authentication required)

**Description:** Register a new teacher account.

**Request Body:**
```json
{
  "username": "teacher1",
  "email": "teacher@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "id": "uuid-here",
  "username": "teacher1",
  "email": "teacher@example.com",
  "role": "teacher",
  "status": "active",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 2. Login
**POST** `/api/v1/user/login`

**Access:** Public (No authentication required)

**Description:** Authenticate user and receive access token.

**Request Body:**
```json
{
  "username": "teacher1",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "username": "teacher1",
    "email": "teacher@example.com",
    "role": "teacher",
    "full_name": "John Doe"
  }
}
```

---

### 3. Get Current User Profile
**GET** `/api/v1/user/me`

**Access:** Authenticated users (Teacher or Admin)

**Description:** Get the authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": "uuid-here",
  "username": "teacher1",
  "email": "teacher@example.com",
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

### 4. Logout
**POST** `/api/v1/user/logout`

**Access:** Authenticated users (Teacher or Admin)

**Description:** Logout current user (client should discard token).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Incorrect username or password"
}
```

### 403 Forbidden
```json
{
  "detail": "User account is inactive"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

