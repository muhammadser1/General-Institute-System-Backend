# Payments API Documentation

## Overview
Payment tracking and reporting endpoints for administrators.

**All endpoints require Admin authentication.**

---

## Endpoints

### 1. Create Payment
**POST** `/api/v1/payments/`

**Access:** Admin only

**Description:** Record a new payment from a student.

**Request Body:**
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

---

### 2. Get Monthly Payments
**GET** `/api/v1/payments/monthly`

**Access:** Admin only

**Description:** Get all payments for a specific month with total calculation.

**Query Parameters (Required):**
- `month`: Month number (1-12)
- `year`: Year (e.g., 2024)

**Query Parameters (Optional):**
- `student_name`: Filter by student name (partial match)

**Example:** `GET /api/v1/payments/monthly?month=1&year=2024&student_name=Ahmad`

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

---

## Payment Amount Rules

- **Minimum Amount:** Greater than 0
- **Decimal Places:** Up to 2 decimal places
- **Currency:** Amounts are in the system's default currency

---

## Common Use Cases

### Get All January 2024 Payments
```
GET /api/v1/payments/monthly?month=1&year=2024
```

### Get Payments for Specific Student in January
```
GET /api/v1/payments/monthly?month=1&year=2024&student_name=Ahmad
```

### Record a New Payment
```json
POST /api/v1/payments/
{
  "student_name": "Sara Ahmed",
  "amount": 500.00,
  "payment_date": "2024-01-25T09:00:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Month and year are required"
}
```

### 403 Forbidden
```json
{
  "detail": "Admin access required"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Notes

- Payments are sorted by payment_date in descending order (newest first)
- Partial name matching is case-insensitive
- Total is calculated as the sum of all filtered payments
- Payment records are permanent (no soft delete)

