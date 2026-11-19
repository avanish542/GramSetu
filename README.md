# 🚀 GRAMSETU V2

## Digital Village Governance, Development & Citizen Services Platform

> **"A Digital Bridge Between Panchayat & People"**

GramSetu V2 is a production-grade digital village governance and citizen engagement platform built with **Python 3.13**, **Django 5.2 LTS**, **Django REST Framework**, **PostgreSQL**, **Redis**, **Celery**, **Tailwind CSS**, and **Leaflet OpenStreetMap**.

---

## 📌 1. Project Overview & Problem Statement

In many Indian Gram Panchayats, villagers lack direct visibility into local village development works, budget allocations, work progress, or active government welfare schemes. Furthermore, submitting complaints or requesting certificates often requires physical visits to the Panchayat office with no real-time status tracking.

**GramSetu V2** bridges this digital divide by allowing villagers to answer:
> *"What is happening in my village?"*

It empowers villagers to track development projects, monitor budgets, apply for certificates online, submit complaints, explore schemes, view village infrastructure on an interactive map, and provide verified citizen feedback.

---

## ✨ 2. Key Features

- **Village Development Tracker**: Filter projects by category (Roads, Drainage, Water, Street Lights, Schools, PHC, etc.), view budgets, spent amounts, completion timeline, and Before/During/After photos.
- **Budget & Financial Transparency**: Visualized Chart.js breakdown of total approved budgets vs expenditures and category-wise spending.
- **Civic Complaint Resolution**: Submit complaints with photo/video upload, receive unique ticket numbers (`CMP-2026-XXXX`), and track status updates (`SUBMITTED` -> `ACKNOWLEDGED` -> `ASSIGNED` -> `IN_PROGRESS` -> `RESOLVED`).
- **Public Service Applications**: Online directory for Residence, Income, Birth, Death, and Water Connection certificates (`APP-2026-XXXX`) with secure file uploads.
- **Strict Document Security**: Private object-level authorization ensures villagers can never access another citizen's private uploaded documents.
- **Government Schemes Directory**: Detailed catalog of housing (PMAY-G), agriculture (PM-KISAN), employment (MGNREGA), pension, and health schemes with direct official links.
- **Interactive Infrastructure Map**: Leaflet OpenStreetMap layer showing markers for Panchayat Bhawan, Schools, PHCs, Water Towers, Handpumps, Solar Streetlights, and Toilets.
- **Panchayat & Sarpanch SaaS Dashboard**: Operational dashboard displaying metric counters, budget analytics, pending complaints queue, and document verification desks.
- **REST API & OpenAPI Docs**: DRF endpoints under `/api/` with Swagger UI documentation at `/api/docs/`.
- **Background Tasks & Caching**: Celery background processing and Redis caching for aggregate statistics.

---

## 🏗️ 3. Architecture & Tech Stack

```text
                                Internet / Browser Client
                                            │
                                     Nginx / Gunicorn
                                            │
                                GramSetu Modular Monolith
                                      (Django 5.2)
                                            │
                  ┌─────────────────────────┼─────────────────────────┐
                  │                         │                         │
          PostgreSQL (Prod)            Redis Cache               Celery Workers
       (SQLite local fallback)     (Aggregates & Stats)      (Notifications & Media)
```

- **Backend**: Python 3.13 + Django 5.2 LTS + Django REST Framework
- **Database**: PostgreSQL (with SQLite compatibility for local dev/testing)
- **Cache**: Redis (`django-redis`)
- **Task Queue**: Celery + Redis
- **Frontend**: Django Templates + Tailwind CSS + Vanilla JS + Leaflet.js + Chart.js
- **API Specs**: `drf-spectacular` (OpenAPI 3.0)
- **Containerization**: Docker & Docker Compose

---

## 📂 4. Project Folder Structure

```text
GramSetu/
├── manage.py
├── config/                  # Django configuration settings & master URL routing
│   ├── settings/            # base.py, development.py, production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── apps/                    # 15 Modular Monolith Django Apps
│   ├── core/                # TimeStampedModel, Base views, health checks (/health/, /ready/), seed command
│   ├── accounts/            # Custom User model, Roles (VILLAGER, PANCHAYAT_ADMIN, SUPER_ADMIN), Auth views
│   ├── village/             # Village, Ward, VillageInfo demographics
│   ├── development/         # DevelopmentProject, ProjectCategory, ProjectImage (BEFORE/DURING/AFTER), Expenses, Timeline
│   ├── complaints/          # Complaint (CMP-YYYY-XXXX), Status workflow, Updates
│   ├── services/            # Panchayat Services & Requirements catalog
│   ├── applications/        # ServiceApplication (APP-YYYY-XXXX), ApplicationDocument, Secure Download
│   ├── schemes/             # Government Schemes, Benefits, Eligibility, Official links
│   ├── notices/             # Panchayat Notices & Announcements
│   ├── gallery/             # Media Gallery & event categories
│   ├── infrastructure/      # Infrastructure map markers (lat/lng for Leaflet map)
│   ├── feedback/            # Verified project ratings & reviews
│   ├── notifications/       # In-App Notifications
│   ├── dashboard/           # Villager, Panchayat Admin, & Super Admin Dashboards
│   └── audit/               # Administrative Audit Log
├── api/                     # DRF Serializers, ViewSets, Routers & OpenAPI schema
├── templates/               # Responsive Tailwind CSS HTML5 templates
├── static/                  # Static assets
├── media/                   # Media uploads
├── tests/                   # Pytest test suite (100% passing)
├── requirements/            # base.txt, development.txt, production.txt
├── Dockerfile & docker-compose.yml
├── locustfile.py            # Locust load testing script
├── pytest.ini
└── README.md
```

---

## 🔑 5. Demo Accounts & Credentials

The seed command creates sample accounts for testing all user roles:

| Role | Username | Password | Access / Capabilities |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin12345` | System-wide admin, audit logs, multi-village settings |
| **Panchayat Admin / Sarpanch** | `sarpanch` | `admin12345` | SaaS Operations Dashboard, complaint queue, doc verification |
| **Villager** | `ramesh` | `pass12345` | Villager portal, submit complaints, apply for services, feedback |

---

## ⚡ 6. Quick Start & Local Installation

### Prerequisites
- Python 3.12+ installed
- Git installed

### 1. Clone & Setup Virtual Environment
```bash
git clone <repository-url> GramSetu
cd GramSetu

python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements/development.txt
```

### 3. Apply Database Migrations
```bash
python manage.py migrate
```

### 4. Seed Demo Data
Populates Rampur Gram Panchayat with 20+ projects, 15+ complaints, 10+ schemes, 10+ notices, 20+ infrastructure map markers, and demo users:
```bash
python manage.py seed_demo_data
```

### 5. Run Development Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🐳 7. Docker Deployment

Deploy the complete stack (Django, PostgreSQL, Redis, Celery, Gunicorn) with Docker Compose:

```bash
docker-compose up --build
```
Access the application at [http://localhost:8000](http://localhost:8000).

---

## 📑 8. API Documentation

GramSetu V2 provides a full REST API for mobile apps and external integration:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

---

## 🧪 9. Automated Testing & Load Testing

### Run Pytest Suite
```bash
pytest
```
Verifies authentication, role properties, document security isolation, complaint workflows, project budget math, and REST API endpoints.

### Run Locust Load Testing
```bash
locust -f locustfile.py
```
Open [http://localhost:8089](http://localhost:8089) to execute concurrent user load scenarios (100, 500, 1000 users).

---

## 🛡️ 10. Security & Document Isolation

- **Private Document Download Endpoint**: `/applications/document/<id>/download/` enforces strict object-level access control. A villager cannot access another citizen's private uploaded document.
- **CSRF & XSS Protection**: Standard Django CSRF tokens on all POST forms and auto-escaped template rendering.
- **Audit Logging**: Administrative state changes are logged in `AuditLog` table with actor, action, timestamp, and IP address.

---

## 📜 11. Government Disclaimer

> *"GramSetu is a digital platform for village information, citizen engagement, application tracking and Panchayat communication. Official government services, certificates, approvals and verifications remain subject to the relevant authorized government department and applicable procedures."*
