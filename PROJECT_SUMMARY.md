# General Institute System - Project Summary

## 🎯 What is it?
Backend API for managing an educational institute - handles teachers, lessons, payments, and pricing.

## 🏗️ Tech Stack
- **Framework:** FastAPI (Python)
- **Database:** MongoDB
- **Auth:** JWT tokens
- **CORS:** Configurable origins

---

## 📡 API Endpoints

### User & Auth
- `POST /api/v1/user/signup` - Teacher registration
- `POST /api/v1/user/login` - Login (get token)
- `GET /api/v1/user/me` - Get current user
- `POST /api/v1/user/logout` - Logout

### Lessons (Teachers)
- `POST /api/v1/lessons/submit` - Submit new lesson
- `GET /api/v1/lessons/my-lessons` - Get my lessons (with filters)
- `GET /api/v1/lessons/{id}` - Get lesson by ID
- `PUT /api/v1/lessons/{id}` - Update lesson
- `DELETE /api/v1/lessons/{id}` - Cancel lesson
- `GET /api/v1/lessons/summary` - Get aggregated statistics

### Admin
- `POST /api/v1/admin/users` - Create user
- `GET /api/v1/admin/users` - Get all users (paginated, filtered)
- `GET /api/v1/admin/users/{id}` - Get user by ID
- `PUT /api/v1/admin/users/{id}` - Update user
- `DELETE /api/v1/admin/users/{id}` - Deactivate user
- `POST /api/v1/admin/users/{id}/reset-password` - Reset password
- `GET /api/v1/admin/teacher-earnings/{id}` - Get teacher earnings report
- `GET /api/v1/admin/subject-prices` - Get subject prices

### Payments (Admin)
- `POST /api/v1/payments/` - Create payment record
- `GET /api/v1/payments/monthly` - Get monthly payments

### Pricing
- `POST /api/v1/pricing/` - Create subject price (Admin)
- `GET /api/v1/pricing/` - Get all pricing (Admin)
- `GET /api/v1/pricing/{id}` - Get pricing by ID (Admin)
- `PUT /api/v1/pricing/{id}` - Update pricing (Admin)
- `DELETE /api/v1/pricing/{id}` - Delete pricing (Admin)
- `GET /api/v1/pricing/lookup/{subject}` - Lookup price (Auth)
- `GET /api/v1/pricing/public/all` - Get public pricing (No auth)

---

## 🗄️ Database Collections
- **users** - Teachers and admins
- **lessons** - Lesson records
- **payments** - Payment tracking
- **pricing** - Subject pricing config

---

## 🛠️ Scripts Available

### Setup & Testing
- `scripts/databases_scriptis/verify_setup.py` - Check system config
- `scripts/databases_scriptis/test_connection.py` - Test MongoDB
- `scripts/databases_scriptis/setup_database.py` - Initialize DB

### Data
- `scripts/populate_sample_data.py` - Create test teacher + 17 lessons

### Testing
- `scripts/run_cors_test.py` - Test CORS with multiple ports

---

## 🔐 Features
- JWT authentication
- Role-based access (Teacher, Admin)
- CORS protection
- Pagination & filtering
- Earnings calculation
- Lesson status tracking (pending, completed, cancelled)
- Subject-based pricing
- Payment tracking

---

## 🎯 Why This Project?
Educational institute needs to:
- Track teacher lessons
- Calculate earnings by subject
- Manage student payments
- Configure subject pricing
- Admin dashboard for reports

---

## 📊 Current Capabilities
✅ Teacher registration & login  
✅ Submit & manage lessons  
✅ Filter lessons by type, subject, status  
✅ Admin user management  
✅ Teacher earnings reports  
✅ Payment tracking  
✅ Subject pricing management  
✅ CORS configuration  

---

## 🚀 How to Run
```bash
# Setup
python scripts/databases_scriptis/verify_setup.py
python scripts/databases_scriptis/setup_database.py
python scripts/populate_sample_data.py

# Start
uvicorn app.main:app --reload
```

---

**Version:** 1.0.0  
**Framework:** FastAPI  
**Database:** MongoDB

