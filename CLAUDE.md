# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Flask + MySQL web app for a second-hand motorcycle dealership ("Supa Auto Link"). Server-rendered Jinja templates, no JS framework. A public catalogue/inquiry site plus a login-protected admin panel for managing bikes, images, inquiries, sales, and business settings.

## Commands

The active virtualenv is `.venv/` (note: a stale `venv/` also exists — use `.venv/`).

```bash
source .venv/bin/activate                 # activate venv
pip install -r requirements.txt           # install deps
python run.py                             # run dev server on http://127.0.0.1:5000
python seed_data.py                       # load sample bikes/inquiries (optional)

pytest                                    # run all tests
pytest tests/test_auth_decorator.py       # run one file
pytest tests/test_auth_decorator.py::test_admin_page_redirects_guest  # run one test
```

Required environment variables (loaded from `.env` via python-dotenv, see `config.py`): `SECRET_KEY`, `MYSQL_PASSWORD` are mandatory and the app raises on startup if unset. Also used: `MYSQL_HOST`/`MYSQL_USER`/`MYSQL_DATABASE`, `SESSION_COOKIE_SECURE`, and `ADMIN_NAME`/`ADMIN_EMAIL`/`ADMIN_PASSWORD` (the last three seed the first admin account — password must be ≥12 chars).

MySQL must be running and reachable. There is no migration tool — schema lives in code (see below).

## Architecture

Layered MVC. Request flow: **Routes (Blueprint classes) → Controllers → Models (extend BaseModel) → Database (raw PyMySQL) → MySQL**.

- **`app/__init__.py`** — `create_app(testing=False)` factory. Wires config, CSRF, rate limiter, upload folder, error handlers (404/413/429), and registers blueprints. When not testing, it calls `Database.ensure_database()` + `Database.create_tables()` at startup.
- **`app/routes/`** — `PublicRoutes` and `AdminRoutes` are *classes* (not module-level functions). Each has `__init__` that builds a `Blueprint` and instantiates its controller, and a `register()` method that maps URLs to controller methods and returns the blueprint. Admin routes wrap handlers with `admin_required`; the login route is additionally wrapped with `limiter.limit(...)`.
- **`app/controllers/`** — `PublicController` / `AdminController`. Instantiate model objects in `__init__` and hold all request handling + template rendering. (`admin_controller_backup.py` is a stale copy — ignore it.)
- **`app/models/`** — Each model (`User`, `Bike`, `Inquiry`, `Settings`) extends `BaseModel` (abstract, requires a `table` property; provides `find_by_id`, `find_all`, `delete_by_id`). Models create a `Database()` per operation and `close()` it. `find_all` whitelists `ORDER BY` columns against `ALLOWED_ORDER_COLUMNS` to prevent SQL injection via sort params.
- **`app/models/database.py`** — Raw PyMySQL wrapper (`fetch_one`/`fetch_all`/`execute`, `autocommit=False`, DictCursor). Also owns the **entire schema**: `create_tables()` defines every table with `CREATE TABLE IF NOT EXISTS`, runs idempotent in-place migrations via `add_column_if_missing`/`MODIFY COLUMN`, seeds default settings row (id=1), and seeds the initial admin. To change the schema, edit `create_tables()` — there is no separate migrations directory.
- **`app/auth.py`** — `admin_required` decorator checks `session["admin_id"]` and `session["role"] == "admin"`, clears stale sessions, and redirects to `admin.login`.
- **`app/extensions.py`** — shared `csrf` (Flask-WTF CSRFProtect) and `limiter` (Flask-Limiter, keyed by remote address) singletons, `init_app`-ed in the factory.

## Conventions

- **SQL safety**: always use parameterized queries (`%s` + params tuple). Table/column names interpolated into f-strings must come from trusted/whitelisted values only (see `BaseModel.find_all` and `ALLOWED_ORDER_COLUMNS`).
- **State-changing routes are POST + CSRF** (logout, delete, toggle, status updates). CSRF tokens must be included in the corresponding forms.
- **Uploads**: bike images go to `app/static/uploads/bikes/` (gitignored except `.gitkeep`), filtered by `config.ALLOWED_IMAGE_EXTENSIONS`, filenames run through `secure_filename`. Max request size is 16 MB (`MAX_CONTENT_LENGTH`).
- **Code style**: the existing code uses a distinctive vertically-spread formatting (one argument per line, blank lines between logical blocks, banner comments). Match the surrounding file's style when editing.
- **Money/sales**: bikes track `purchase_price`, `additional_expenses`, `sold_price`, `sold_date` — profit reporting (`/admin/sales`, CSV export) is computed from these.
