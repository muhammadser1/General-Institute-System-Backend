# Backend API Reference for Frontend Integration

> **Complete API documentation for frontend developers**
> 
> **Base URL:** `http://localhost:8000/api/v1` (development)  
> **Production URL:** Update this when deploying

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
   - [User & Authentication](#1-user--authentication)
   - [Lessons Management](#2-lessons-management)
   - [Admin Operations](#3-admin-operations)
   - [Payments](#4-payments)
   - [Pricing](#5-pricing)
4. [Error Handling](#error-handling)
5. [Data Models](#data-models)
6. [Common Workflows](#common-workflows)

---

## Quick Start

### 1. Authentication Flow

```javascript
// Step 1: Login to get access token
const loginResponse = await fetch('http://localhost:8000/api/v1/user/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'teacher1',
    password: 'password123'
  })
});

const { access_token, user } = await loginResponse.json();

// Step 2: Store token (use secure storage in production)
localStorage.setItem('access_token', access_token);

// Step 3: Use token in subsequent requests
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${access_token}`
};
```

### 2. Making Authenticated Requests

```javascript
// Example: Get current user profile
const response = await fetch('http://localhost:8000/api/v1/user/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

const userData = await response.json();
```

---

## Authentication

### Login
**POST** `/user/login`

**Access:** Public

**Request:**
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

### Signup (Teacher Registration)
**POST** `/user/signup`

**Access:** Public

**Request:**
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

### Get Current User
**GET** `/user/me`

**Access:** Authenticated

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

### Logout
**POST** `/user/logout`

**Access:** Authenticated

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

---

## API Endpoints

## 1. User & Authentication

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/user/signup` | Public | Register new teacher |
| POST | `/user/login` | Public | Login and get token |
| GET | `/user/me` | Auth | Get current user profile |
| POST | `/user/logout` | Auth | Logout user |

---

## 2. Lessons Management

### Submit New Lesson
**POST** `/lessons/submit`

**Access:** Teacher

**Request:**
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

### Get My Lessons
**GET** `/lessons/my-lessons`

**Access:** Teacher or Admin

**Query Parameters:**
- `lesson_type` (optional): `individual` or `group`
- `status` (optional): `pending`, `completed`, `cancelled`
- `subject` (optional): Subject name

**Example:** `/lessons/my-lessons?lesson_type=individual&status=completed`

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

### Get Lesson by ID
**GET** `/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin

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

### Update Lesson
**PUT** `/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin

**Note:** Can only update pending lessons

**Request:**
```json
{
  "subject": "Physics",
  "duration_minutes": 90,
  "scheduled_date": "2024-01-21T11:00:00Z",
  "notes": "Updated notes",
  "status": "completed"
}
```

**Response (200):** Same as Get Lesson by ID

### Delete/Cancel Lesson
**DELETE** `/lessons/{lesson_id}`

**Access:** Teacher (own lessons) or Admin

**Response (200):**
```json
{
  "message": "Lesson cancelled successfully"
}
```

### Get Lessons Summary
**GET** `/lessons/summary`

**Access:** Teacher or Admin

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

### Lessons Endpoints Summary

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/lessons/submit` | Teacher | Submit new lesson |
| GET | `/lessons/my-lessons` | Teacher/Admin | Get all lessons with filters |
| GET | `/lessons/{id}` | Teacher/Admin | Get lesson by ID |
| PUT | `/lessons/{id}` | Teacher/Admin | Update lesson |
| DELETE | `/lessons/{id}` | Teacher/Admin | Cancel lesson |
| GET | `/lessons/summary` | Teacher/Admin | Get aggregated statistics |

---

## 3. Admin Operations

### User Management

#### Create User
**POST** `/admin/users`

**Access:** Admin only

**Request:**
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

#### Get All Users
**GET** `/admin/users`

**Access:** Admin only

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 50, max: 100)
- `role` (optional): `teacher` or `admin`
- `status` (optional): `active`, `inactive`, `suspended`

**Example:** `/admin/users?role=teacher&limit=20`

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

#### Get User by ID
**GET** `/admin/users/{user_id}`

**Access:** Admin only

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

#### Update User
**PUT** `/admin/users/{user_id}`

**Access:** Admin only

**Request:**
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

**Response (200):** Same as Get User by ID

#### Deactivate User
**DELETE** `/admin/users/{user_id}`

**Access:** Admin only

**Response (200):**
```json
{
  "message": "User deactivated successfully"
}
```

#### Reset User Password
**POST** `/admin/users/{user_id}/reset-password`

**Access:** Admin only

**Request:**
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

### Reports & Earnings

#### Get Teacher Earnings
**GET** `/admin/teacher-earnings/{teacher_id}`

**Access:** Admin only

**Query Parameters:**
- `month` (optional): 1-12
- `year` (optional): Year

**Example:** `/admin/teacher-earnings/uuid?month=1&year=2024`

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

#### Get Subject Prices
**GET** `/admin/subject-prices`

**Access:** Admin only

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

### Admin Endpoints Summary

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/admin/users` | Admin | Create user |
| GET | `/admin/users` | Admin | Get all users with filters |
| GET | `/admin/users/{id}` | Admin | Get user by ID |
| PUT | `/admin/users/{id}` | Admin | Update user |
| DELETE | `/admin/users/{id}` | Admin | Deactivate user |
| POST | `/admin/users/{id}/reset-password` | Admin | Reset user password |
| GET | `/admin/teacher-earnings/{id}` | Admin | Get teacher earnings |
| GET | `/admin/subject-prices` | Admin | Get subject prices |

---

## 4. Payments

### Create Payment
**POST** `/payments/`

**Access:** Admin only

**Request:**
```json
{
  "student_name": "Ahmad Ali",
  "amount": 250.00,
  "payment_date": "2024-01-15T10:00:00Z",
  "lesson_id": "lesson-uuid",
  "notes": "Monthly payment for January"
}
```

**Response (201):**
```json
{
  "id": "payment-uuid",
  "student_name": "Ahmad Ali",
  "amount": 250.00,
  "payment_date": "2024-01-15T10:00:00Z",
  "lesson_id": "lesson-uuid",
  "notes": "Monthly payment for January",
  "created_at": "2024-01-15T10:05:00Z"
}
```

### Get Monthly Payments
**GET** `/payments/monthly`

**Access:** Admin only

**Query Parameters (Required):**
- `month`: 1-12
- `year`: Year (e.g., 2024)

**Query Parameters (Optional):**
- `student_name`: Filter by student name (partial match)

**Example:** `/payments/monthly?month=1&year=2024&student_name=Ahmad`

**Response (200):**
```json
{
  "payments": [
    {
      "id": "payment-uuid-1",
      "student_name": "Ahmad Ali",
      "amount": 250.00,
      "payment_date": "2024-01-15T10:00:00Z",
      "lesson_id": "lesson-uuid-1",
      "notes": "Monthly payment for January",
      "created_at": "2024-01-15T10:05:00Z"
    },
    {
      "id": "payment-uuid-2",
      "student_name": "Ahmad Ali",
      "amount": 100.00,
      "payment_date": "2024-01-20T14:00:00Z",
      "lesson_id": "lesson-uuid-2",
      "notes": "Additional lesson payment",
      "created_at": "2024-01-20T14:05:00Z"
    }
  ],
  "total": 350.00,
  "month": 1,
  "year": 2024,
  "count": 2
}
```

### Payments Endpoints Summary

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/payments/` | Admin | Create payment record |
| GET | `/payments/monthly` | Admin | Get monthly payments |

---

## 5. Pricing

### Admin Pricing Management

#### Create Subject Price
**POST** `/pricing/`

**Access:** Admin only

**Request:**
```json
{
  "subject": "Chemistry",
  "individual_price": 30.00,
  "group_price": 28.00,
  "currency": "USD"
}
```

**Response (201):**
```json
{
  "id": "pricing-uuid",
  "subject": "Chemistry",
  "individual_price": 30.00,
  "group_price": 28.00,
  "currency": "USD",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Get All Pricing
**GET** `/pricing/`

**Access:** Admin only

**Query Parameters:**
- `is_active` (optional): `true` or `false`

**Example:** `/pricing/?is_active=true`

**Response (200):**
```json
{
  "pricing": [
    {
      "id": "pricing-uuid-1",
      "subject": "Math",
      "individual_price": 25.00,
      "group_price": 25.00,
      "currency": "USD",
      "is_active": true,
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-10T08:00:00Z"
    }
  ],
  "total": 1
}
```

#### Get Pricing by ID
**GET** `/pricing/{pricing_id}`

**Access:** Admin only

**Response (200):** Same as Create Subject Price

#### Update Pricing
**PUT** `/pricing/{pricing_id}`

**Access:** Admin only

**Request:**
```json
{
  "individual_price": 32.00,
  "group_price": 30.00,
  "is_active": true
}
```

**Response (200):** Same as Get Pricing by ID

#### Delete/Deactivate Pricing
**DELETE** `/pricing/{pricing_id}`

**Access:** Admin only

**Response (200):**
```json
{
  "message": "Pricing deactivated successfully"
}
```

### User Pricing Lookup

#### Lookup Subject Price
**GET** `/pricing/lookup/{subject}`

**Access:** Authenticated users

**Example:** `/pricing/lookup/Math`

**Response (200):**
```json
{
  "subject": "Math",
  "individual_price": 25.00,
  "group_price": 25.00,
  "currency": "USD"
}
```

**Response (404) - Subject Not Found:**
```json
{
  "subject": "UnknownSubject",
  "individual_price": 25.00,
  "group_price": 25.00,
  "currency": "USD",
  "note": "Using default pricing"
}
```

### Public Pricing

#### Get All Public Pricing
**GET** `/pricing/public/all`

**Access:** Public (No authentication required)

**Response (200):**
```json
{
  "pricing": [
    {
      "subject": "Math",
      "individual_price": 25.00,
      "group_price": 25.00,
      "currency": "USD"
    },
    {
      "subject": "Physics",
      "individual_price": 25.00,
      "group_price": 25.00,
      "currency": "USD"
    },
    {
      "subject": "Chemistry",
      "individual_price": 30.00,
      "group_price": 28.00,
      "currency": "USD"
    }
  ],
  "default_individual_price": 25.00,
  "default_group_price": 25.00,
  "currency": "USD",
  "total": 3
}
```

### Pricing Endpoints Summary

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/pricing/` | Admin | Create subject price |
| GET | `/pricing/` | Admin | Get all pricing |
| GET | `/pricing/{id}` | Admin | Get pricing by ID |
| PUT | `/pricing/{id}` | Admin | Update pricing |
| DELETE | `/pricing/{id}` | Admin | Deactivate pricing |
| GET | `/pricing/lookup/{subject}` | Auth | Lookup subject price |
| GET | `/pricing/public/all` | Public | Get all public pricing |

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Request validation failed |
| 500 | Server Error | Internal server error |

### Error Response Formats

#### Standard Error (400, 401, 403, 404, 500)
```json
{
  "detail": "Error message here"
}
```

#### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

### Common Error Messages

| Error | Status | Description |
|-------|--------|-------------|
| "Username already exists" | 400 | Username is taken |
| "Incorrect username or password" | 401 | Invalid credentials |
| "Admin access required" | 403 | User lacks admin privileges |
| "Not authorized to access this lesson" | 403 | User can't access this resource |
| "User not found" | 404 | User ID doesn't exist |
| "Lesson not found" | 404 | Lesson ID doesn't exist |
| "Cannot update completed lesson" | 400 | Lesson already completed |
| "Month and year are required" | 400 | Missing required query params |
| "Subject pricing already exists" | 400 | Subject already has pricing |

### Error Handling Example (JavaScript)

```javascript
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = await response.json();
      
      switch (response.status) {
        case 401:
          // Token expired or invalid
          localStorage.removeItem('access_token');
          window.location.href = '/login';
          break;
        case 403:
          // Insufficient permissions
          alert('You do not have permission to perform this action');
          break;
        case 404:
          // Resource not found
          alert('Resource not found');
          break;
        case 422:
          // Validation error
          const validationErrors = error.detail;
          console.error('Validation errors:', validationErrors);
          break;
        default:
          alert(error.detail || 'An error occurred');
      }
      
      throw error;
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}
```

---

## Data Models

### User Model
```typescript
interface User {
  id: string;
  username: string;
  email: string;
  role: "teacher" | "admin";
  status: "active" | "inactive" | "suspended";
  first_name: string;
  last_name: string;
  phone: string;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
  last_login?: string; // ISO 8601
}
```

### Lesson Model
```typescript
interface Lesson {
  id: string;
  teacher_id: string;
  teacher_name: string;
  subject: string;
  lesson_type: "individual" | "group";
  duration_minutes: number;
  scheduled_date: string; // ISO 8601
  status: "pending" | "completed" | "cancelled";
  students: Student[];
  notes?: string;
  created_at: string; // ISO 8601
  updated_at?: string; // ISO 8601
  completed_at?: string; // ISO 8601
}

interface Student {
  name: string;
  grade: string;
}
```

### Payment Model
```typescript
interface Payment {
  id: string;
  student_name: string;
  amount: number;
  payment_date: string; // ISO 8601
  lesson_id?: string;
  notes?: string;
  created_at: string; // ISO 8601
}
```

### Pricing Model
```typescript
interface Pricing {
  id: string;
  subject: string;
  individual_price: number;
  group_price: number;
  currency: string;
  is_active: boolean;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}
```

### Teacher Earnings Model
```typescript
interface TeacherEarnings {
  teacher_id: string;
  teacher_name: string;
  month: number;
  year: number;
  total_lessons: number;
  total_hours: number;
  total_earnings: number;
  by_subject: SubjectEarnings[];
}

interface SubjectEarnings {
  subject: string;
  lesson_type: "individual" | "group";
  lesson_count: number;
  total_hours: number;
  price_per_hour: number;
  total_amount: number;
}
```

---

## Common Workflows

### 1. Teacher Login & Submit Lesson

```javascript
// Step 1: Login
const loginResponse = await fetch('http://localhost:8000/api/v1/user/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'teacher1',
    password: 'password123'
  })
});

const { access_token } = await loginResponse.json();
localStorage.setItem('access_token', access_token);

// Step 2: Submit lesson
const lessonResponse = await fetch('http://localhost:8000/api/v1/lessons/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    subject: 'Math',
    lesson_type: 'individual',
    duration_minutes: 60,
    scheduled_date: new Date().toISOString(),
    students: [
      { name: 'Ahmad Ali', grade: 'Grade 10' }
    ],
    notes: 'Covered algebra basics'
  })
});

const lesson = await lessonResponse.json();
console.log('Lesson created:', lesson);
```

### 2. Get Teacher's Lessons with Filters

```javascript
const token = localStorage.getItem('access_token');

// Get completed individual lessons
const response = await fetch(
  'http://localhost:8000/api/v1/lessons/my-lessons?lesson_type=individual&status=completed',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

const { lessons, total_lessons, total_hours } = await response.json();
console.log(`Found ${total_lessons} lessons (${total_hours} hours)`);
```

### 3. Admin: Get All Users with Pagination

```javascript
const token = localStorage.getItem('access_token');

// Get first 20 teachers
const response = await fetch(
  'http://localhost:8000/api/v1/admin/users?role=teacher&limit=20&skip=0',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

const { users, total, limit, skip } = await response.json();
console.log(`Showing ${users.length} of ${total} users`);
```

### 4. Admin: Get Teacher Earnings Report

```javascript
const token = localStorage.getItem('access_token');
const teacherId = 'teacher-uuid';
const month = 1;
const year = 2024;

const response = await fetch(
  `http://localhost:8000/api/v1/admin/teacher-earnings/${teacherId}?month=${month}&year=${year}`,
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

const earnings = await response.json();
console.log(`Total earnings: $${earnings.total_earnings}`);
console.log(`Total hours: ${earnings.total_hours}`);
```

### 5. Admin: Create Payment Record

```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/v1/payments/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    student_name: 'Ahmad Ali',
    amount: 250.00,
    payment_date: new Date().toISOString(),
    notes: 'Monthly payment for January'
  })
});

const payment = await response.json();
console.log('Payment recorded:', payment);
```

### 6. Get Public Pricing (No Auth Required)

```javascript
const response = await fetch('http://localhost:8000/api/v1/pricing/public/all');
const { pricing, default_individual_price, default_group_price } = await response.json();

console.log('Available subjects:', pricing.map(p => p.subject));
console.log('Default price:', default_individual_price);
```

### 7. Update Lesson Status

```javascript
const token = localStorage.getItem('access_token');
const lessonId = 'lesson-uuid';

const response = await fetch(`http://localhost:8000/api/v1/lessons/${lessonId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    status: 'completed',
    notes: 'Lesson completed successfully'
  })
});

const updatedLesson = await response.json();
console.log('Lesson updated:', updatedLesson);
```

---

## Best Practices

### 1. Token Management
```javascript
// Store token securely
localStorage.setItem('access_token', token);

// Check if token exists before making requests
const token = localStorage.getItem('access_token');
if (!token) {
  // Redirect to login
  window.location.href = '/login';
}

// Handle token expiration
if (response.status === 401) {
  localStorage.removeItem('access_token');
  window.location.href = '/login';
}
```

### 2. Date Formatting
```javascript
// Always use ISO 8601 format for dates
const now = new Date().toISOString(); // "2024-01-20T14:30:00.000Z"

// Parse dates from API
const scheduledDate = new Date(lesson.scheduled_date);
const formattedDate = scheduledDate.toLocaleDateString();
```

### 3. Error Handling
```javascript
// Always check response status
if (!response.ok) {
  const error = await response.json();
  console.error('API Error:', error.detail);
  // Handle error appropriately
}
```

### 4. Loading States
```javascript
// Show loading indicator during API calls
setLoading(true);
try {
  const data = await fetchData();
  setData(data);
} catch (error) {
  setError(error.message);
} finally {
  setLoading(false);
}
```

### 5. Pagination
```javascript
// Implement pagination for large datasets
const [page, setPage] = useState(0);
const limit = 20;

const fetchUsers = async () => {
  const response = await fetch(
    `/api/v1/admin/users?skip=${page * limit}&limit=${limit}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.json();
};
```

---

## Interactive API Documentation

The backend provides interactive documentation via Swagger UI and ReDoc:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- Browse all available endpoints
- View request/response schemas
- Test endpoints directly from the browser
- Authenticate and try protected endpoints

---

## Support & Contact

For issues or questions:
- Check the detailed endpoint documentation above
- Review error messages for validation details
- Consult the interactive API docs at `/docs`
- Contact the backend team for assistance

---

## Quick Reference Card

### Public Endpoints (No Auth)
- `POST /user/signup` - Register teacher
- `POST /user/login` - Login
- `GET /pricing/public/all` - Get public pricing

### Teacher Endpoints (Auth Required)
- `GET /user/me` - Get profile
- `POST /user/logout` - Logout
- `POST /lessons/submit` - Submit lesson
- `GET /lessons/my-lessons` - Get my lessons
- `GET /lessons/{id}` - Get lesson by ID
- `PUT /lessons/{id}` - Update lesson
- `DELETE /lessons/{id}` - Cancel lesson
- `GET /lessons/summary` - Get summary
- `GET /pricing/lookup/{subject}` - Lookup price

### Admin Endpoints (Admin Auth Required)
- All Teacher endpoints +
- `POST /admin/users` - Create user
- `GET /admin/users` - Get all users
- `GET /admin/users/{id}` - Get user by ID
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Deactivate user
- `POST /admin/users/{id}/reset-password` - Reset password
- `GET /admin/teacher-earnings/{id}` - Get earnings
- `GET /admin/subject-prices` - Get prices
- `POST /payments/` - Create payment
- `GET /payments/monthly` - Get monthly payments
- `POST /pricing/` - Create pricing
- `GET /pricing/` - Get all pricing
- `GET /pricing/{id}` - Get pricing by ID
- `PUT /pricing/{id}` - Update pricing
- `DELETE /pricing/{id}` - Delete pricing

---

**Last Updated:** January 2024  
**API Version:** v1  
**Backend Framework:** FastAPI (Python)

