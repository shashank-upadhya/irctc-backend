## IRCTC Railway Booking System

A complete railway reservation backend API with JWT authentication, dual database architecture (MySQL + MongoDB Atlas), and real-time booking management.

## Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- MongoDB Atlas account

### Installation

```bash
# 1. Clone & Setup
git clone <repo-url>
cd irctc_backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Create MySQL database
mysql -u root -p
CREATE DATABASE irctc_db;
EXIT;

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser(email='admin@irctc.com', name='Admin', password='admin123', is_admin=True)
exit()

# 7. Start server
python manage.py runserver
```

Server runs at: **http://localhost:8000**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register user |
| POST | `/api/login/` | Login |
| GET | `/api/trains/search/?source=X&destination=Y` | Search trains |
| POST | `/api/trains/` | Create/update train |
| POST | `/api/bookings/` | Book seats |
| GET | `/api/bookings/my/` | Get bookings |
| GET | `/api/analytics/top-routes/` | Top 5 routes |

---

## 🔧 Sample API Calls

### 1. Register User

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secure123"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "tokens": {
    "access": "eyJ0eXAi...",
    "refresh": "eyJ0eXAi..."
  }
}
```

---

### 2. Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@irctc.com",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "email": "admin@irctc.com",
    "is_admin": true
  },
  "tokens": {
    "access": "eyJ0eXAi...",
    "refresh": "eyJ0eXAi..."
  }
}
```

**💡 Save the `access` token for next requests!**

---

### 3. Search Trains

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:8000/api/trains/search/?source=Delhi&destination=Mumbai"
```

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "train_number": "12301",
      "train_name": "Rajdhani Express",
      "source": "Delhi",
      "destination": "Mumbai",
      "departure_time": "16:30:00",
      "arrival_time": "08:30:00",
      "available_seats": 500,
      "fare": "2500.00"
    }
  ]
}
```

---

### 4. Create Train (Admin Only)

```bash
curl -X POST http://localhost:8000/api/trains/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "train_number": "12345",
    "train_name": "Chennai Express",
    "source": "Chennai",
    "destination": "Bangalore",
    "departure_time": "14:30:00",
    "arrival_time": "20:00:00",
    "total_seats": 400,
    "available_seats": 400,
    "fare": "800.00",
    "is_active": true
  }'
```

**Response:**
```json
{
  "message": "Train created successfully",
  "train": {
    "train_number": "12345",
    "train_name": "Chennai Express",
    ...
  }
}
```

---

### 5. Book Train

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "train_id": 1,
    "seats_booked": 2,
    "booking_date": "2026-02-15"
  }'
```

**Response:**
```json
{
  "message": "Booking confirmed successfully",
  "booking": {
    "booking_id": "a1b2c3d4-...",
    "train": {
      "train_number": "12301",
      "train_name": "Rajdhani Express",
      ...
    },
    "seats_booked": 2,
    "total_fare": "5000.00",
    "status": "CONFIRMED"
  }
}
```

---

### 6. Get My Bookings

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:8000/api/bookings/my/"
```

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "booking_id": "a1b2c3d4-...",
      "train": {
        "train_number": "12301",
        ...
      },
      "seats_booked": 2,
      "total_fare": "5000.00",
      "status": "CONFIRMED"
    }
  ]
}
```

---

### 7. Top Routes Analytics

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "http://localhost:8000/api/analytics/top-routes/"
```

**Response:**
```json
{
  "top_routes": [
    {
      "source": "Delhi",
      "destination": "Mumbai",
      "search_count": 15,
      "avg_execution_time": 0.0234,
      "last_searched": "2026-01-08T..."
    },
    ...
  ],
  "total_routes_analyzed": 5
}
```

---

## 🗄️ Database Schema

### MySQL (`irctc_db`)

**Users Table:**
- id, email, password, name, is_admin, created_at

**Trains Table:**
- id, train_number, train_name, source, destination, departure_time, arrival_time, total_seats, available_seats, fare

**Bookings Table:**
- id, booking_id, user_id, train_id, seats_booked, booking_date, total_fare, status

### MongoDB Atlas (`irctc_analytics`)

**api_logs Collection:**
- endpoint, method, params, user_id, execution_time, timestamp, source, destination

---

## Testing with Postman

1. Import collection
2. Set environment variable: `base_url` = `http://localhost:8000/api`
3. Test in order: Register → Login → Search → Book → Analytics

---

## Default Admin Credentials

- **Email:** admin@irctc.com
- **Password:** admin123

**Change these after first login!**