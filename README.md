# Supa Auto Link — Flask MVC

This is the Flask/MySQL conversion of the supplied Figma/React motorcycle dealership prototype.

## Architecture

The project follows the same MVC-style pattern as the earlier Library Management System:

```text
Browser / Jinja Templates
        ↓
Routes (Blueprint classes)
        ↓
Controllers
        ↓
Models / BaseModel
        ↓
Database (PyMySQL)
        ↓
MySQL
```

### Public side — no login
- Home page
- Available bike catalogue
- Search / brand / category / price filters
- Bike details + image gallery
- About page
- Contact page
- Customer inquiry form

### Admin side — login required
- Dashboard
- Add bike
- Edit bike
- Delete bike
- Mark Available / Sold
- Upload cover + gallery images
- View and update customer inquiries
- Update business settings

## Project structure

```text
Supa_Auto_Link_Flask/
├── app/
│   ├── controllers/
│   │   ├── public_controller.py
│   │   └── admin_controller.py
│   ├── models/
│   │   ├── base_model.py
│   │   ├── database.py
│   │   ├── user.py
│   │   ├── bike.py
│   │   ├── inquiry.py
│   │   └── settings.py
│   ├── routes/
│   │   ├── public.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── public/
│   │   ├── admin/
│   │   └── partials/
│   └── static/
│       ├── images/
│       ├── css/
│       ├── js/
│       └── uploads/bikes/
├── config.py
├── run.py
├── seed_data.py
└── requirements.txt
```

## macOS setup

```bash
cd Supa_Auto_Link_Flask
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Edit `config.py` or provide environment variables for your MySQL credentials:

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "YOUR_PASSWORD"
MYSQL_DATABASE = "supa_auto_link"
```

The app creates the database and tables automatically if the MySQL user has permission.

Optional sample data:

```bash
python seed_data.py
```

Run:

```bash
python run.py
```

Public site:

```text
http://127.0.0.1:5000/
```

Admin:

```text
http://127.0.0.1:5000/admin/login
```

Development admin created automatically:

```text
Email: admin@supautolink.com
Password: admin123
```

**Change this password before deploying to a real server.**

## Original React → Flask mapping

| React | Flask |
|---|---|
| `App.tsx` state/navigation | Flask routes + controller redirects |
| `sampleBikes` | MySQL `bikes` table |
| `sampleInquiries` | MySQL `inquiries` table |
| `Home.tsx` | `templates/public/home.html` |
| `AvailableBikes.tsx` | `templates/public/bikes.html` |
| `BikeDetails.tsx` | `templates/public/bike_detail.html` |
| `AdminLogin.tsx` | `templates/admin/login.html` |
| `Dashboard.tsx` | `templates/admin/dashboard.html` |
| `AllBikes.tsx` | `templates/admin/bikes.html` |
| `AddBike.tsx` | `templates/admin/bike_form.html` |
| React state CRUD | Controller → Model → MySQL |
