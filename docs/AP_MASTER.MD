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

<!-- **User Endpoints:**
- `GET /api/v1/pricing/lookup/{subject}` - Lookup subject price (Authenticated)

**Public Endpoints:**
- `GET /api/v1/pricing/public/all` - Get all public pricing (No auth) -->

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