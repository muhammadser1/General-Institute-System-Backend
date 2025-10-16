# 💰 Database-Driven Pricing System

Complete pricing management system with database storage and admin API endpoints.

---

## 🎯 **What Was Created:**

### **1. Database Model**
- ✅ **`app/models/pricing.py`** - Pricing model for MongoDB
  - Stores subject name, individual price, group price, currency
  - Business logic methods: `get_price()`, `calculate_earnings()`
  - Database methods: `find_by_subject()`, `get_all_active()`, `save()`, `update_in_db()`, `delete()`

### **2. API Schemas**
- ✅ **`app/schemas/pricing.py`** - Pydantic schemas for request/response
  - `PricingCreate` - Create new pricing
  - `PricingUpdate` - Update existing pricing
  - `PricingResponse` - API response format
  - `PricingListResponse` - List of pricing
  - `PricingLookupResponse` - Price lookup response

### **3. Admin Endpoints**
- ✅ **`app/api/v1/endpoints/pricing.py`** - Full CRUD API
  - **Admin Only:** Create, Read, Update, Delete pricing
  - **Authenticated Users:** Lookup prices
  - **Public:** View all active pricing

### **4. Database Integration**
- ✅ **`app/db/mongodb.py`** - Added `pricing_collection`
  - Created indexes for `subject` (unique) and `is_active`
  - Initialized in database connection

### **5. Updated Core Pricing**
- ✅ **`app/core/pricing.py`** - Now uses DATABASE instead of hardcoded values
  - `get_subject_price()` - Fetches from database
  - `calculate_subject_earnings()` - Calculates with database prices
  - `get_all_subject_prices()` - Returns all from database

---

## 📊 **Database Schema:**

```javascript
{
  "_id": "uuid-string",
  "subject": "Mathematics",           // Unique, case-insensitive
  "individual_price": 50.0,          // Price per hour for individual lessons
  "group_price": 30.0,               // Price per hour for group lessons  
  "currency": "USD",                 // Currency code
  "is_active": true,                 // Active/inactive status
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-20T15:30:00"
}
```

---

## 🔌 **API Endpoints:**

### **Admin Endpoints (Require Admin Auth)**

#### **1. Create Pricing**
```http
POST /api/v1/pricing/
Authorization: Bearer <admin_token>

{
  "subject": "Mathematics",
  "individual_price": 50.0,
  "group_price": 30.0,
  "currency": "USD"
}
```

**Response:**
```json
{
  "id": "abc-123",
  "subject": "Mathematics",
  "individual_price": 50.0,
  "group_price": 30.0,
  "currency": "USD",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00",
  "updated_at": null
}
```

---

#### **2. Get All Pricing**
```http
GET /api/v1/pricing/
Authorization: Bearer <admin_token>

# Optional query params:
?include_inactive=true  # Include inactive pricing
```

**Response:**
```json
{
  "total": 5,
  "pricing": [
    {
      "id": "abc-123",
      "subject": "Mathematics",
      "individual_price": 50.0,
      "group_price": 30.0,
      "currency": "USD",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00",
      "updated_at": null
    },
    // ... more pricing
  ]
}
```

---

#### **3. Get Pricing by ID**
```http
GET /api/v1/pricing/{pricing_id}
Authorization: Bearer <admin_token>
```

---

#### **4. Update Pricing**
```http
PUT /api/v1/pricing/{pricing_id}
Authorization: Bearer <admin_token>

{
  "individual_price": 55.0,
  "group_price": 35.0
}
```

**All fields are optional in update:**
- `subject`
- `individual_price`
- `group_price`
- `currency`
- `is_active`

---

#### **5. Delete Pricing**
```http
DELETE /api/v1/pricing/{pricing_id}
Authorization: Bearer <admin_token>
```

**Response:** 204 No Content

---

### **User Endpoints (Require Auth)**

#### **6. Lookup Price by Subject**
```http
GET /api/v1/pricing/lookup/{subject}?lesson_type=individual
Authorization: Bearer <any_token>
```

**Response:**
```json
{
  "subject": "Mathematics",
  "lesson_type": "individual",
  "price_per_hour": 50.0,
  "currency": "USD",
  "found": true
}
```

---

### **Public Endpoints (No Auth Required)**

#### **7. Get All Active Pricing (Public)**
```http
GET /api/v1/pricing/public/all
```

**Response:**
```json
[
  {
    "id": "abc-123",
    "subject": "Mathematics",
    "individual_price": 50.0,
    "group_price": 30.0,
    "currency": "USD",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": null
  },
  // ... more subjects
]
```

---

## 💡 **Usage Examples:**

### **Admin Creates Pricing**

```python
import requests

# Login as admin
login = requests.post(
    "http://localhost:8000/api/v1/user/login",
    json={"username": "mhmdd400", "password": "mhmdd400"}
)
admin_token = login.json()["access_token"]

# Create pricing for Mathematics
pricing = requests.post(
    "http://localhost:8000/api/v1/pricing/",
    headers={"Authorization": f"Bearer {admin_token}"},
    json={
        "subject": "Mathematics",
        "individual_price": 50.0,
        "group_price": 30.0,
        "currency": "USD"
    }
)
print(pricing.json())
```

---

### **Teacher Looks Up Price**

```python
# Login as teacher
login = requests.post(
    "http://localhost:8000/api/v1/user/login",
    json={"username": "teacher1", "password": "teacher123"}
)
teacher_token = login.json()["access_token"]

# Lookup Mathematics individual price
price = requests.get(
    "http://localhost:8000/api/v1/pricing/lookup/Mathematics?lesson_type=individual",
    headers={"Authorization": f"Bearer {teacher_token}"}
)
print(price.json())
# Output: {"subject": "Mathematics", "lesson_type": "individual", "price_per_hour": 50.0, ...}
```

---

### **Public Page Displays Pricing**

```python
# No authentication needed
pricing = requests.get("http://localhost:8000/api/v1/pricing/public/all")
print(pricing.json())
```

---

## 🔄 **Migration from Hardcoded to Database:**

The old `pricing.py` had hardcoded prices. Now it uses the database!

### **Before (Hardcoded):**
```python
SUBJECT_PRICES = {
    "math": {"individual": 50.0, "group": 30.0},
    "arabic": {"individual": 60.0, "group": 35.0},
    # ... hardcoded values
}
```

### **After (Database-Driven):**
```python
def get_subject_price(subject: str, lesson_type: str = "individual") -> float:
    # Fetches from MongoDB
    pricing = Pricing.find_by_subject(subject, mongo_db.pricing_collection)
    if pricing:
        return pricing.get_price(lesson_type)
    return DEFAULT_PRICE  # Fallback
```

---

## 🎯 **Benefits:**

✅ **Flexible** - No code changes to update prices  
✅ **Admin Control** - Admins manage through API  
✅ **Different Prices** - Individual vs Group pricing  
✅ **Multi-Currency** - Support for different currencies  
✅ **Active/Inactive** - Can disable subjects without deleting  
✅ **Audit Trail** - Track when pricing was created/updated  
✅ **Unique Subjects** - Database ensures no duplicates  
✅ **Fast Lookups** - Indexed for performance  

---

## 📝 **Initial Setup:**

### **1. Populate Initial Pricing (Admin)**

```bash
# Login as admin and create pricing for common subjects
curl -X POST "http://localhost:8000/api/v1/pricing/" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Mathematics",
    "individual_price": 50.0,
    "group_price": 30.0,
    "currency": "USD"
  }'
```

### **2. Bulk Create Script**

Create a script to populate initial pricing:

```python
subjects = [
    ("Mathematics", 50.0, 30.0),
    ("Physics", 55.0, 33.0),
    ("Chemistry", 55.0, 33.0),
    ("Biology", 50.0, 30.0),
    ("English", 55.0, 32.0),
    ("Arabic", 60.0, 35.0),
    ("Programming", 65.0, 40.0),
]

for subject, individual, group in subjects:
    requests.post(
        "http://localhost:8000/api/v1/pricing/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "subject": subject,
            "individual_price": individual,
            "group_price": group,
            "currency": "USD"
        }
    )
```

---

## ✅ **Next Steps:**

1. ✅ **Run your FastAPI server**
2. ✅ **Login as admin** (mhmdd400)
3. ✅ **Create pricing** for your subjects
4. ✅ **Test lookups** with teachers
5. ✅ **Display public pricing** on frontend

---

**Now you have a complete, production-ready pricing management system!** 🎉

