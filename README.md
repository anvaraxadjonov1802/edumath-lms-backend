# EduMath LMS Backend

EduMath LMS — iqtisodchilar uchun matematika fanini o‘rganishga mo‘ljallangan ta’lim platformasining backend qismi.

Platforma orqali talabalar nazariy materiallarni o‘qishi, amaliy topshiriqlar bilan ishlashi, test yechishi, natijalarini ko‘rishi, glossariy va foydalanilgan adabiyotlardan foydalanishi mumkin.

---

## Project Overview

Ushbu loyiha ta’lim jarayonini raqamlashtirish uchun ishlab chiqilgan backend tizimidir. Backend orqali kurslar, qismlar, mavzular, nazariy va amaliy materiallar, testlar, test natijalari, glossariy va adabiyotlar boshqariladi.

Loyiha Django REST Framework asosida qurilgan bo‘lib, frontend qismi keyinchalik React, Vue yoki boshqa frontend texnologiya orqali ulanadi.

---

## Main Purpose

Loyihaning asosiy maqsadi:

- talabaga mavzularni bosqichma-bosqich o‘rganish imkonini berish;
- nazariy bilimlarni PDF yoki boshqa fayllar orqali taqdim etish;
- amaliy topshiriqlarni platforma orqali ko‘rsatish;
- test orqali bilimni tekshirish;
- natijalarni avtomatik hisoblash;
- o‘quv materiallarini yagona tizimda boshqarish.

---

## Features

### Authentication

- Email orqali ro‘yxatdan o‘tish
- Email verification code orqali tasdiqlash
- Verification code qayta yuborish
- Email va password orqali login
- JWT access token
- JWT refresh token
- Foydalanuvchi profili
- Admin va student rollari

### Learning Content

- Kurslar
- Qismlar
- Mavzular
- Nazariy materiallar
- Amaliy materiallar
- Prezentatsiyalar
- Mustaqil ishlar
- Adabiyotlar
- Fayl yuklash imkoniyati

### Test System

- Mavzuga tegishli test savollari
- Har bir savol uchun bir nechta javob variantlari
- To‘g‘ri javoblarni public API’da yashirish
- Student javoblarini qabul qilish
- Avtomatik tekshirish
- Ball hisoblash
- Foiz hisoblash
- Baholash tizimi
- Student natijalari tarixi

### Additional Features

- Glossariy
- Foydalanilgan adabiyotlar
- Search imkoniyati
- Pagination
- Swagger API documentation
- ReDoc API documentation
- Seed data command
- Admin panel

---

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- drf-spectacular
- django-cors-headers
- python-dotenv
- Pillow
- SQLite for local development

---

## Project Structure

```text
edumath-lms-backend/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── courses/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── seed_initial_data.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── asgi.py
│   ├── pagination.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Database Models

### Accounts app

Main model:

```text
User
```

User fields:

```text
email
full_name
role
is_email_verified
verification_code
verification_code_created_at
is_staff
is_active
```

---

### Courses app

Main models:

```text
Course
Module
Topic
Material
Question
Answer
TestResult
Reference
GlossaryTerm
```

Model vazifalari:

| Model | Description |
|---|---|
| Course | Asosiy kurs |
| Module | Kurs qismlari, masalan 1-qism, 2-qism |
| Topic | Mavzular |
| Material | Nazariy, amaliy, prezentatsiya va boshqa fayllar |
| Question | Test savollari |
| Answer | Test javob variantlari |
| TestResult | Student test natijalari |
| Reference | Foydalanilgan adabiyotlar |
| GlossaryTerm | Glossariy atamalari |

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/edumath-lms-backend.git
cd edumath-lms-backend
```

`YOUR_USERNAME` o‘rniga o‘z GitHub username’ingizni yozing.

---

### 2. Create virtual environment

Windows CMD:

```bash
python -m venv venv
venv\Scripts\activate
```

Windows Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Virtual environment yoqilgandan keyin terminal oldida shunga o‘xshash yozuv chiqadi:

```text
(venv)
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Project root papkasida `.env` fayl yarating.

```text
edumath-lms-backend/
├── .env
├── manage.py
├── config/
├── accounts/
└── courses/
```

`.env.example` fayldan nusxa olish:

Windows CMD:

```bash
copy .env.example .env
```

Git Bash / Linux / macOS:

```bash
cp .env.example .env
```

---

## Example `.env`

```env
SECRET_KEY=django-insecure-edumath-local-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=EduMath LMS <noreply@edumath.uz>
```

---

## Important Security Notes

`.env` fayl GitHub’ga push qilinmasligi kerak.

GitHub’ga faqat quyidagi fayl chiqadi:

```text
.env.example
```

Quyidagilar GitHub’ga chiqmasligi kerak:

```text
.env
db.sqlite3
media/
venv/
```

---

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

Bu loyiha email authentication ishlatadi. Shuning uchun username emas, email so‘raydi.

Example:

```text
Email: admin@gmail.com
Password: ********
Password again: ********
```

Agar password oddiy bo‘lsa, Django ogohlantiradi. Local development uchun `y` bosib davom ettirish mumkin.

---

## Seed Initial Data

Demo kurs, qismlar, mavzular, test savollari, glossariy va adabiyotlarni yaratish uchun:

```bash
python manage.py seed_initial_data
```

Bu command quyidagilarni yaratadi:

```text
Course:
Iqtisodchilar uchun matematika

Modules:
1-qism
2-qism

Demo topics:
Matritsalar
Determinantlar
Chiziqli tenglamalar sistemasi
Vektorlar
Analitik geometriya
Sonli ketma-ketliklar
Funksiyalar
Limit
Hosila

Demo:
Test savollari
Javob variantlari
Glossariy
Adabiyotlar
```

---

## Run Development Server

```bash
python manage.py runserver
```

Server ishga tushgandan keyin:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

Swagger API docs:

```text
http://127.0.0.1:8000/api/docs/
```

ReDoc API docs:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

## API Documentation

Backendda API dokumentatsiya uchun Swagger va ReDoc qo‘shilgan.

### Swagger UI

```text
GET /api/docs/
```

Swagger orqali API’larni brauzerdan test qilish mumkin.

### ReDoc

```text
GET /api/redoc/
```

ReDoc orqali API documentation chiroyli ko‘rinishda ochiladi.

### OpenAPI Schema

```text
GET /api/schema/
```

---

# API Endpoints

---

## Auth API

### Register

```http
POST /api/auth/register/
```

Body:

```json
{
  "email": "student@gmail.com",
  "full_name": "Test Student",
  "password": "student12345"
}
```

Response:

```json
{
  "id": 1,
  "email": "student@gmail.com",
  "full_name": "Test Student"
}
```

Local development holatida verification code terminalda chiqadi.

---

### Verify Email

```http
POST /api/auth/verify-email/
```

Body:

```json
{
  "email": "student@gmail.com",
  "code": "123456"
}
```

Response:

```json
{
  "message": "Email muvaffaqiyatli tasdiqlandi"
}
```

---

### Resend Verification Code

```http
POST /api/auth/resend-code/
```

Body:

```json
{
  "email": "student@gmail.com"
}
```

Response:

```json
{
  "message": "Yangi tasdiqlash kodi yuborildi"
}
```

---

### Login

```http
POST /api/auth/login/
```

Body:

```json
{
  "email": "student@gmail.com",
  "password": "student12345"
}
```

Response:

```json
{
  "message": "Login muvaffaqiyatli bajarildi",
  "refresh": "refresh_token",
  "access": "access_token",
  "user": {
    "id": 1,
    "email": "student@gmail.com",
    "full_name": "Test Student",
    "role": "student",
    "is_email_verified": true
  }
}
```

---

### Profile

```http
GET /api/auth/profile/
```

Header:

```http
Authorization: Bearer ACCESS_TOKEN
```

Response:

```json
{
  "id": 1,
  "email": "student@gmail.com",
  "full_name": "Test Student",
  "role": "student",
  "is_email_verified": true
}
```

---

## Course API

### Course List

```http
GET /api/courses/
```

Response:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Iqtisodchilar uchun matematika",
      "slug": "iqtisodchilar-uchun-matematika",
      "description": "Ushbu kurs iqtisodiyot yo‘nalishida tahsil oluvchi talabalar uchun...",
      "image": null,
      "image_url": null,
      "modules_count": 2,
      "topics_count": 9,
      "created_at": "2026-05-07T10:00:00Z"
    }
  ]
}
```

---

### Course Search

```http
GET /api/courses/?search=matematika
```

---

### Course Detail

```http
GET /api/courses/{slug}/
```

Example:

```http
GET /api/courses/iqtisodchilar-uchun-matematika/
```

Response ichida course, modules va topics nested holatda chiqadi.

---

## Topic API

### Topic List

```http
GET /api/topics/
```

---

### Filter Topics by Course

```http
GET /api/topics/?course=1
```

---

### Filter Topics by Module

```http
GET /api/topics/?module=1
```

---

### Search Topics

```http
GET /api/topics/?search=matritsa
```

---

### Topic Detail

```http
GET /api/topics/{id}/
```

Example:

```http
GET /api/topics/1/
```

Response:

```json
{
  "id": 1,
  "title": "1-mavzu: Matritsalar va ular ustida amallar",
  "slug": "1-mavzu-matritsalar-va-ular-ustida-amallar",
  "description": "Matritsa tushunchasi, matritsalar turlari...",
  "order": 1,
  "module": 1,
  "module_title": "1-qism",
  "course_title": "Iqtisodchilar uchun matematika",
  "materials": [],
  "questions_count": 3
}
```

---

## Material API

### Topic Materials

```http
GET /api/topics/{topic_id}/materials/
```

Example:

```http
GET /api/topics/1/materials/
```

---

### Filter Materials by Type

Nazariy materiallar:

```http
GET /api/topics/1/materials/?type=theory
```

Amaliy materiallar:

```http
GET /api/topics/1/materials/?type=practice
```

Prezentatsiyalar:

```http
GET /api/topics/1/materials/?type=presentation
```

Mustaqil ishlar:

```http
GET /api/topics/1/materials/?type=assignment
```

Adabiyotlar:

```http
GET /api/topics/1/materials/?type=literature
```

Boshqa materiallar:

```http
GET /api/topics/1/materials/?type=other
```

---

## Material Types

```text
theory        — Nazariy qism
practice      — Amaliy qism
presentation  — Prezentatsiya
assignment    — Mustaqil ish
literature    — Adabiyot
other         — Boshqa
```

---

## Test API

### Get Topic Questions

```http
GET /api/topics/{topic_id}/questions/
```

Example:

```http
GET /api/topics/1/questions/
```

Response:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "text": "Matritsa nima?",
      "order": 1,
      "answers": [
        {
          "id": 1,
          "text": "Sonlar yoki matematik ifodalardan tashkil topgan to‘g‘ri to‘rtburchak shaklidagi jadval."
        },
        {
          "id": 2,
          "text": "Faqat bitta sondan iborat matematik ifoda."
        }
      ]
    }
  ]
}
```

Important:

```text
Correct answer public API’da chiqmaydi.
```

---

### Submit Test

```http
POST /api/topics/{topic_id}/submit-test/
```

Header:

```http
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json
```

Body:

```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_id": 1
    },
    {
      "question_id": 2,
      "answer_id": 5
    },
    {
      "question_id": 3,
      "answer_id": 9
    }
  ]
}
```

Response:

```json
{
  "message": "Test muvaffaqiyatli yakunlandi",
  "result": {
    "id": 1,
    "topic": 1,
    "topic_title": "1-mavzu: Matritsalar va ular ustida amallar",
    "module_title": "1-qism",
    "course_title": "Iqtisodchilar uchun matematika",
    "score": 3,
    "total_questions": 3,
    "percentage": 100.0,
    "grade": "A'lo",
    "created_at": "2026-05-07T10:00:00Z"
  },
  "summary": {
    "score": 3,
    "total_questions": 3,
    "answered_questions": 3,
    "percentage": 100.0
  }
}
```

---

### My Test Results

```http
GET /api/my-results/
```

Header:

```http
Authorization: Bearer ACCESS_TOKEN
```

Response:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "topic": 1,
      "topic_title": "1-mavzu: Matritsalar va ular ustida amallar",
      "module_title": "1-qism",
      "course_title": "Iqtisodchilar uchun matematika",
      "score": 3,
      "total_questions": 3,
      "percentage": 100.0,
      "grade": "A'lo",
      "created_at": "2026-05-07T10:00:00Z"
    }
  ]
}
```

---

## Grade System

Test natijasi foiz asosida baholanadi:

```text
90 - 100  => A'lo
70 - 89   => Yaxshi
50 - 69   => Qoniqarli
0 - 49    => Qoniqarsiz
```

---

## Glossary API

### Glossary List

```http
GET /api/glossary/
```

---

### Glossary Search

```http
GET /api/glossary/?search=limit
```

Response:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "term_uz": "Limit",
      "term_en": "Limit",
      "term_ru": "Предел",
      "definition": "Limit — argument ma’lum qiymatga yaqinlashganda funksiya qiymatining qanday qiymatga yaqinlashishini ifodalaydi."
    }
  ]
}
```

---

## References API

### References List

```http
GET /api/references/
```

---

### References Search

```http
GET /api/references/?search=matematika
```

Response:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Iqtisodchilar uchun matematika",
      "author": "O‘quv-uslubiy qo‘llanma",
      "year": "2024",
      "link": "",
      "file": null,
      "file_url": null,
      "description": "Iqtisodiyot yo‘nalishi talabalari uchun matematika faniga oid nazariy va amaliy materiallar."
    }
  ]
}
```

---

## Pagination

List API endpointlar pagination bilan ishlaydi.

Example:

```http
GET /api/topics/?page=1&page_size=5
```

Response format:

```json
{
  "count": 20,
  "next": "http://127.0.0.1:8000/api/topics/?page=2&page_size=5",
  "previous": null,
  "results": []
}
```

Default page size:

```text
10
```

Maximum page size:

```text
50
```

---

## Search Support

Search mavjud endpointlar:

```text
GET /api/courses/?search=...
GET /api/topics/?search=...
GET /api/glossary/?search=...
GET /api/references/?search=...
```

---

## Swagger Authorization

Swagger’da login talab qiladigan endpointlarni test qilish uchun:

1. `/api/auth/login/` orqali login qiling.
2. Response ichidan `access` tokenni copy qiling.
3. Swagger yuqorisidagi `Authorize` tugmasini bosing.
4. Tokenni quyidagi formatda kiriting:

```text
Bearer ACCESS_TOKEN
```

Example:

```text
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

Shundan keyin quyidagi endpointlarni Swagger’dan test qilish mumkin:

```text
GET /api/auth/profile/
POST /api/topics/{topic_id}/submit-test/
GET /api/my-results/
```

---

## Admin Panel

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

Admin panel orqali quyidagilar boshqariladi:

```text
Users
Courses
Modules
Topics
Materials
Questions
Answers
Test Results
References
Glossary Terms
```

---

## Useful Commands

Run server:

```bash
python manage.py runserver
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Seed demo data:

```bash
python manage.py seed_initial_data
```

Update requirements:

```bash
pip freeze > requirements.txt
```

Check git status:

```bash
git status
```

Commit changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

---

## Git Workflow

Tavsiya qilinadigan workflow:

```bash
git status
git add .
git commit -m "Meaningful commit message"
git push
```

Commit message namunalari:

```text
Initial Django backend setup
Add email authentication with JWT
Add core LMS models and admin
Add course content API endpoints
Add test submission and results API
Add pagination and API improvements
Configure environment variables and security settings
Add Swagger and ReDoc API documentation
Fix Swagger request body schemas
Add project README documentation
```

---

## Local Development Flow

Loyihani localda ishga tushirish tartibi:

```bash
git clone https://github.com/YOUR_USERNAME/edumath-lms-backend.git
cd edumath-lms-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_initial_data
python manage.py runserver
```

Git Bash ishlatsangiz:

```bash
git clone https://github.com/YOUR_USERNAME/edumath-lms-backend.git
cd edumath-lms-backend

python -m venv venv
source venv/Scripts/activate

pip install -r requirements.txt

cp .env.example .env

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_initial_data
python manage.py runserver
```

---

## Notes

- `.env` private saqlanishi kerak.
- `db.sqlite3` GitHub’ga push qilinmaydi.
- `media/` GitHub’ga push qilinmaydi.
- `venv/` GitHub’ga push qilinmaydi.
- Local email verification code terminalda chiqadi.
- Deploy paytida real SMTP email service ulanadi.
- Frontend uchun CORS sozlamalari `.env` orqali boshqariladi.

---

## Current Project Status

Backend qismi frontend ulashga tayyor.

Completed:

```text
Authentication
Email verification
JWT login
User profile
Course models
Course APIs
Topic APIs
Material APIs
Test question APIs
Test submit API
My results API
Glossary API
References API
Pagination
Search
Swagger documentation
ReDoc documentation
Seed data command
Admin panel
Environment variables
GitHub README
```

---

## Next Steps

Keyingi bosqichlar:

```text
Frontend development
React / Vite project setup
Login/Register pages
Course list page
Topic detail page
PDF/material viewer
Test page
Result page
Profile page
Admin dashboard frontend
Deployment
```

---

## Author

Developed as an educational LMS backend project for mathematics learning platform.


Project theme:

```text
Iqtisodchilar uchun matematika ta’lim platformasi
```