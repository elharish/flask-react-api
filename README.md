# Flask React App — Project Setup Guide

A full-stack web application built with **React.js** (frontend), **Python Flask** (backend), and **MySQL** (database).

---

## Prerequisites

Make sure the following software is installed on your machine before running the project.

### 1. Python
- **Version:** Python 3.9 or higher
- **Download:** https://www.python.org/downloads/
- Verify installation:
  ```bash
  python --version
  ```

### 2. Node.js & npm
- **Version:** Node.js 18 or higher
- **Download:** https://nodejs.org/
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

### 3. MySQL Server
- **Version:** MySQL 8.0 or higher
- **Download:** https://dev.mysql.com/downloads/mysql/
- Verify installation:
  ```bash
  mysql --version
  ```

---

## Project Structure

```
flask-react-app/
│
├── backend/                   # Python Flask API
│   ├── app.py                 # Application entry point
│   ├── config.py              # Database & JWT configuration
│   ├── extensions.py          # Flask extensions (db, bcrypt)
│   ├── models.py              # SQLAlchemy User model
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (credentials)
│   └── routes/
│       ├── __init__.py
│       └── auth.py            # API routes: /register, /login, /me
│
├── frontend/                  # React.js (Vite)
│   ├── index.html
│   ├── package.json           # Node dependencies
│   └── src/
│       ├── main.jsx           # React entry point
│       ├── App.jsx            # Route definitions
│       ├── index.css          # Global styles
│       ├── components/
│       │   └── PrivateRoute.jsx
│       └── pages/
│           ├── Login.jsx
│           ├── Register.jsx
│           └── Dashboard.jsx
│
└── README.md                  # This file
```

---

## Step-by-Step Setup

### Step 1 — Create the MySQL Database

Open your MySQL terminal and run:

```sql
CREATE DATABASE IF NOT EXISTS flask_auth_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Or via command line (replace `yourpassword`):

```bash
mysql -u root -pyourpassword -e "CREATE DATABASE IF NOT EXISTS flask_auth_db;"
```

---

### Step 2 — Configure Environment Variables

Open `backend/.env` and fill in your MySQL credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=flask_auth_db
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production
```

> **Important:** Change `JWT_SECRET_KEY` to a long random string before deploying to production.

---

### Step 3 — Install Backend Dependencies

Navigate to the `backend` folder and install Python packages:

```bash
cd backend
pip install -r requirements.txt
```

#### Python packages installed:

| Package | Version | Purpose |
|---|---|---|
| Flask | 3.0.3 | Web framework |
| Flask-CORS | 4.0.1 | Cross-Origin Resource Sharing |
| Flask-SQLAlchemy | 3.1.1 | ORM for MySQL |
| PyMySQL | 1.1.1 | MySQL database driver |
| Flask-Bcrypt | 1.0.1 | Password hashing |
| PyJWT | 2.8.0 | JSON Web Token authentication |
| python-dotenv | 1.0.1 | Load `.env` variables |
| cryptography | 42.0.8 | Cryptographic backend |

---

### Step 4 — Install Frontend Dependencies

Navigate to the `frontend` folder and install Node packages:

```bash
cd frontend
npm install
```

#### Key Node packages installed:

| Package | Purpose |
|---|---|
| react | UI library |
| react-dom | DOM rendering |
| react-router-dom | Client-side routing |
| axios | HTTP requests to Flask API |
| lucide-react | SVG icon library |
| vite | Development server & bundler |

---

## Running the Project

You need **two terminals** running simultaneously — one for the backend and one for the frontend.

### Terminal 1 — Start Flask Backend

```bash
cd flask-react-app/backend
python app.py
```

The backend will start at: **http://localhost:5000**

Expected output:
```
[OK] Database tables are ready.
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Terminal 2 — Start React Frontend

```bash
cd flask-react-app/frontend
npm run dev
```

The frontend will start at: **http://localhost:5173**

Expected output:
```
  VITE ready in 300ms
  Local: http://localhost:5173/
```

---

## Accessing the Application

Open your browser and go to:

```
http://localhost:5173
```

### Pages

| URL | Description |
|---|---|
| `/login` | Login page (default) |
| `/register` | Registration page |
| `/dashboard` | User dashboard (requires login) |

---

## API Endpoints Reference

Base URL: `http://localhost:5000/api`

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/register` | No | Create a new user account |
| `POST` | `/login` | No | Login and receive JWT token |
| `GET` | `/me` | Yes (Bearer token) | Get current logged-in user data |

### Example — Register

```json
POST /api/register
{
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "password": "secret123",
  "confirm_password": "secret123"
}
```

### Example — Login

```json
POST /api/login
{
  "email": "john@example.com",
  "password": "secret123"
}
```

Response:
```json
{
  "token": "<JWT token>",
  "message": "Login successful!"
}
```

### Example — Get Current User

```http
GET /api/me
Authorization: Bearer <JWT token>
```

Response:
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "mobile": "9876543210",
    "email": "john@example.com",
    "created_at": "09 June 2026, 12:00 PM"
  }
}
```

> **Note:** Password is never returned by any API endpoint.

---

## Database Schema

Table: **`users`** (auto-created on first backend startup)

| Column | Type | Details |
|---|---|---|
| `id` | INT | Primary key, auto-increment |
| `name` | VARCHAR(120) | User's full name |
| `mobile` | VARCHAR(20) | Phone number |
| `email` | VARCHAR(150) | Unique, used for login |
| `password` | VARCHAR(255) | bcrypt hashed (never exposed) |
| `created_at` | DATETIME | Auto-set on registration |

---

## Common Issues & Fixes

### MySQL Access Denied
Check your credentials in `backend/.env`. Make sure `DB_USER`, `DB_PASSWORD` and `DB_NAME` are correct.

### Port Already in Use
- Flask default port is `5000` — kill any process using it or change the port in `app.py`.
- Vite default port is `5173` — it will auto-select the next available port.

### CORS Error in Browser
Ensure the Flask backend is running and the `CORS` origin in `app.py` matches `http://localhost:5173`.

### Token Expired / Unauthorized
JWT tokens expire after **24 hours**. Simply log in again to get a new token.

---

## Tech Stack Summary

| Layer | Technology |
|---|---|
| Frontend | React.js 18, Vite, React Router, Axios, Lucide React |
| Backend | Python 3, Flask 3, Flask-SQLAlchemy, Flask-Bcrypt, PyJWT |
| Database | MySQL 8 |
| Auth | JWT (JSON Web Tokens) stored in localStorage |
| Styling | Vanilla CSS — Dark glassmorphism theme |
