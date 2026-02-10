# 📸 Photographer Assignment System (Django REST API)

## 📌 Project Overview
The **Photographer Assignment System** is a Django REST Framework–based backend application that manages events and photographers, with a **smart auto-assignment feature**.  
The system automatically assigns photographers to events based on availability, activity status, and scheduling constraints, while handling edge cases safely.

This project was built as part of a **Backend Intern Assignment** to demonstrate backend design, REST API development, and clean coding practices.

---

## 🛠️ Tech Stack
- **Python 3.10**
- **Django 5.1.2**
- **Django REST Framework**
- **SQLite**
- **flake8** (for PEP8 checks)

---

## 📂 Project Structure

```text
photographer_assignment/
│
├── management/                  # Main application
│   ├── models.py                # Event, Photographer, Assignment models
│   ├── views.py                 # API logic & smart assignment
│   ├── serializers.py           # DRF serializers
│   ├── urls.py                  # API routes
│   └── migrations/
│
├── photographer_assignment/     # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── manage.py
├── db.sqlite3
└── README.md
```

---

## 🧱 Data Models

### Event
- `event_name` (CharField)
- `event_date` (DateField)
- `photographers_required` (IntegerField)
- `created_at` (DateTimeField)

### Photographer
- `name` (CharField)
- `email` (EmailField, unique)
- `phone` (CharField)
- `is_active` (BooleanField)

### Assignment
- `event` (ForeignKey → Event)
- `photographer` (ForeignKey → Photographer)

A separate **Assignment** model is used to correctly represent the many-to-many relationship and avoid duplicate or conflicting assignments.

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/vanshaggarwal27/EventGraphia
cd photographer_assignment
```

### 2️⃣ Create & activate a virtual environment
```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install django djangorestframework flake8
```

### 4️⃣ Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the server
```bash
python manage.py runserver
```

Open in browser: http://127.0.0.1:8000/

---

## 🔗 API Endpoints

### 📅 Events

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/events/` | List all events |
| POST | `/api/events/` | Create a new event |
| GET | `/api/events/<id>/` | Event details with assignments |
| PUT | `/api/events/<id>/` | Update event |
| DELETE | `/api/events/<id>/` | Delete event |
| POST | `/api/events/<id>/assign-photographers/` | Auto-assign photographers |
| GET | `/api/events/<id>/assignments/` | Get assigned photographers |

### 📷 Photographers

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/photographers/` | List all photographers |
| POST | `/api/photographers/` | Create photographer |
| GET | `/api/photographers/<id>/` | Photographer details |
| PUT | `/api/photographers/<id>/` | Update photographer |
| DELETE | `/api/photographers/<id>/` | Delete photographer |
| GET | `/api/photographers/<id>/schedule/` | Photographer’s schedule |

---

## 🧠 Smart Assignment Logic

When `POST /api/events/<id>/assign-photographers/` is called:

### Validations
- Event date must not be in the past
- `photographers_required` must be greater than 0
- Event must not already have assignments

### Selection Rules
- Photographer must be active
- Photographer must not be assigned to another event on the same date

### Assignment
- Exactly the required number of photographers is assigned
- Assignment records are created atomically
- Assigned photographer details are returned

---

## ⚠️ Edge Case Handling

### ❌ Not enough photographers
- Request is rejected
- No partial assignments are created
- Returns **400 Bad Request**

```json
{
  "error": "Not enough photographers available"
}
```

### ❌ Event already assigned

```json
{
  "error": "Photographers already assigned to this event"
}
```

---

## 🧪 Testing
All APIs can be tested using **Django REST Framework’s Browsable API**.

Example:  
http://127.0.0.1:8000/api/events/1/assign-photographers/

Leave the form empty and click **POST**.

---

## 🧹 Code Quality
- Follows **PEP8** guidelines
- Checked using **flake8**
- Django-generated files excluded from linting
- Clean separation of concerns
- Descriptive variable and method names

### Run linting
```bash
python -m flake8
```

