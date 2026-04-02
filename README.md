# Finance Data Processing Backend

## Overview

I built this backend to simulate a finance dashboard system where users interact with financial data based on their roles.

The goal was to design a clean and structured backend that handles:
- User authentication
- Role-based access control
- Financial record management
- Dashboard analytics

Instead of adding unnecessary complexity, I focused on making the system logically organized and easy to extend.

---

## Tech Stack

- FastAPI (Python)
- MongoDB (Motor)
- JWT Authentication
- Pydantic (Validation)

---

## Features

### User & Role Management
- Register and login users
- Roles: Admin, Analyst, Viewer
- Role-based restrictions enforced at API level

### Financial Records
- Create, view, and soft delete records
- Filtering by type and category
- Each record linked to a user

### Dashboard APIs
- Total Income
- Total Expenses
- Net Balance
- Monthly Trends (using MongoDB aggregation)

### Access Control
- Admin → full access  
- Analyst → read + analytics  
- Viewer → read-only  

---

## API Endpoints

### Auth
- POST `/auth/register`
- POST `/auth/login`

### Records
- POST `/records/` (Admin)
- GET `/records/` (Admin, Analyst)
- DELETE `/records/{id}` (Admin)

### Dashboard
- GET `/dashboard/summary`
- GET `/dashboard/trends`

---

## How to Run

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload