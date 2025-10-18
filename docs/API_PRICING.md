# Pricing API Documentation

## Overview
Subject pricing management and lookup endpoints.

---

## Admin Endpoints (Pricing Management)

### 1. Create Subject Price
**POST** `/api/v1/pricing/`

**Access:** Admin only

**Description:** Create or configure pricing for a specific subject.

**Request Body:**
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

---

### 2. Get All Pricing
**GET** `/api/v1/pricing/`

**Access:** Admin only

**Description:** Get all subject pricing configurations.

**Query Parameters:**
- `is_active` (optional): Filter by active status (true/false)

**Example:** `GET /api/v1/pricing/?is_active=true`

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
    },
    {
      "id": "pricing-uuid-2",
      "subject": "Chemistry",
      "individual_price": 30.00,
      "group_price": 28.00,
      "currency": "USD",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 2
}
```

---

### 3. Get Pricing by ID
**GET** `/api/v1/pricing/{pricing_id}`

**Access:** Admin only

**Description:** Get specific pricing configuration by ID.

**Response (200):**
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

---

### 4. Update Pricing
**PUT** `/api/v1/pricing/{pricing_id}`

**Access:** Admin only

**Description:** Update pricing configuration for a subject.

**Request Body:**
```json
{
  "individual_price": 32.00,
  "group_price": 30.00,
  "is_active": true
}
```

**Response (200):**
```json
{
  "id": "pricing-uuid",
  "subject": "Chemistry",
  "individual_price": 32.00,
  "group_price": 30.00,
  "currency": "USD",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T14:00:00Z"
}
```

---

### 5. Delete Pricing (Deactivate)
**DELETE** `/api/v1/pricing/{pricing_id}`

**Access:** Admin only

**Description:** Deactivate pricing for a subject (soft delete).

**Response (200):**
```json
{
  "message": "Pricing deactivated successfully"
}
```

---

## User Endpoints (Pricing Lookup)

### 6. Lookup Subject Price
**GET** `/api/v1/pricing/lookup/{subject}`

**Access:** Authenticated users (Teacher or Admin)

**Description:** Look up pricing for a specific subject.

**Example:** `GET /api/v1/pricing/lookup/Math`

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

---

## Public Endpoints

### 7. Get All Public Pricing
**GET** `/api/v1/pricing/public/all`

**Access:** Public (No authentication required)

**Description:** Get all active subject pricing (public view).

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

---

## Pricing Rules

- **Subject names** are case-sensitive
- **Unique constraint** on subject names
- **Prices** must be greater than 0
- **Decimal precision** up to 2 decimal places
- **Default pricing** is used when subject is not found (25.00 for both types)
- **Soft delete** - deactivated pricing is preserved but not shown in public/lookup

---

## Common Use Cases

### Add New Subject Pricing
```json
POST /api/v1/pricing/
{
  "subject": "Biology",
  "individual_price": 28.00,
  "group_price": 26.00
}
```

### Update Existing Pricing
```json
PUT /api/v1/pricing/{pricing_id}
{
  "individual_price": 35.00,
  "group_price": 32.00
}
```

### Check Price for a Subject
```
GET /api/v1/pricing/lookup/Chemistry
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Subject pricing already exists"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 404 Not Found
```json
{
  "detail": "Pricing configuration not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "individual_price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

