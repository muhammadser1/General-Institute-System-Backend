# API Documentation Index

## Overview
Complete API documentation for the General Institute System Backend.

**Base URL:** `http://localhost:8000` (development)

---

## API Endpoints by Category

### 📋 [User API](./API_USER.md)
Authentication and user profile management.

**Endpoints:**
- `POST /api/v1/user/signup` - Teacher registration
- `POST /api/v1/user/login` - User login
- `GET /api/v1/user/me` - Get current user profile
- `POST /api/v1/user/logout` - Logout

**Access:** Public (signup, login) | Authenticated (profile, logout)

---

### 👨‍💼 [Admin API](./API_ADMIN.md)
Administrative operations for user management and reporting.

**Endpoints:**
- `POST /api/v1/admin/users` - Create user
- `GET /api/v1/admin/users` - Get all users
- `GET /api/v1/admin/users/{id}` - Get user by ID
- `PUT /api/v1/admin/users/{id}` - Update user
- `DELETE /api/v1/admin/users/{id}` - Deactivate user
- `POST /api/v1/admin/users/{id}/reset-password` - Reset password
- `GET /api/v1/admin/teacher-earnings/{id}` - Get teacher earnings
- `GET /api/v1/admin/subject-prices` - Get subject prices

**Access:** Admin only

---

### 📚 [Lessons API](./API_LESSONS.md)
Lesson submission and management for teachers.

**Endpoints:**
- `POST /api/v1/lessons/submit` - Submit new lesson
- `GET /api/v1/lessons/my-lessons` - Get my lessons
- `GET /api/v1/lessons/{id}` - Get lesson by ID
- `PUT /api/v1/lessons/{id}` - Update lesson
- `DELETE /api/v1/lessons/{id}` - Cancel lesson
- `GET /api/v1/lessons/summary` - Get lessons summary

**Access:** Teacher (own lessons) | Admin (all lessons)

---

### 💰 [Payments API](./API_PAYMENTS.md)
Payment tracking and reporting.

**Endpoints:**
- `POST /api/v1/payments/` - Create payment record
- `GET /api/v1/payments/monthly` - Get monthly payments

**Access:** Admin only

---

### 💵 [Pricing API](./API_PRICING.md)
Subject pricing management and lookup.

**Admin Endpoints:**
- `POST /api/v1/pricing/` - Create subject price
- `GET /api/v1/pricing/` - Get all pricing
- `GET /api/v1/pricing/{id}` - Get pricing by ID
- `PUT /api/v1/pricing/{id}` - Update pricing
- `DELETE /api/v1/pricing/{id}` - Deactivate pricing

**User Endpoints:**
- `GET /api/v1/pricing/lookup/{subject}` - Lookup subject price (Authenticated)

**Public Endpoints:**
- `GET /api/v1/pricing/public/all` - Get all public pricing (No auth)

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

Get your access token by calling the login endpoint:

```bash
POST /api/v1/user/login
{
  "username": "your_username",
  "password": "your_password"
}
```

---

## Role-Based Access Control

| Role | Access Level |
|------|-------------|
| **Admin** | Full access to all endpoints |
| **Teacher** | Access to lessons, profile, and pricing lookup |
| **Public** | Access to signup, login, and public pricing |

---

## Response Formats

### Success Response
```json
{
  "id": "uuid",
  "field": "value",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

### Validation Error (422)
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

---

## HTTP Status Codes

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

---

## API Testing

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/user/login \
  -H "Content-Type: application/json" \
  -d '{"username": "teacher1", "password": "password123"}'
```

**Submit Lesson:**
```bash
curl -X POST http://localhost:8000/api/v1/lessons/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "subject": "Math",
    "lesson_type": "individual",
    "duration_minutes": 60,
    "scheduled_date": "2024-01-20T14:00:00Z",
    "students": [{"name": "Ahmad Ali", "grade": "Grade 10"}]
  }'
```

### Using Python Requests

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/user/login",
    json={"username": "teacher1", "password": "password123"}
)
token = response.json()["access_token"]

# Submit lesson
headers = {"Authorization": f"Bearer {token}"}
lesson_data = {
    "subject": "Math",
    "lesson_type": "individual",
    "duration_minutes": 60,
    "scheduled_date": "2024-01-20T14:00:00Z",
    "students": [{"name": "Ahmad Ali", "grade": "Grade 10"}]
}
response = requests.post(
    "http://localhost:8000/api/v1/lessons/submit",
    json=lesson_data,
    headers=headers
)
```

---

## Interactive API Documentation

The API provides interactive documentation via Swagger UI and ReDoc:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- Browse all available endpoints
- View request/response schemas
- Test endpoints directly from the browser
- Authenticate and try protected endpoints

---

## Rate Limiting & Best Practices

1. **Token Management:** Store tokens securely and refresh when expired
2. **Error Handling:** Always check response status codes
3. **Pagination:** Use skip/limit parameters for large datasets
4. **Date Formats:** Use ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
5. **Validation:** Validate data client-side before sending requests

---

## Support

For issues or questions:
- Check the detailed endpoint documentation
- Review error messages for validation details
- Consult the interactive API docs at `/docs`

