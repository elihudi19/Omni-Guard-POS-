# Omni-Guard POS & Inventory API

> SaaS backend for Bar, Agricultural Shop, Hardware, and Restaurant businesses in Tanzania.  
> Built with Django REST Framework · PostgreSQL on Render · Offline-capable design.

---

## Features

| Feature | Description |
|---|---|
| **Automated Margin Pricing** | Manager enters purchase price → Admin sets margin % → Retail price auto-calculated |
| **Role-Based Access** | Admin / Manager / Cashier — scoped permissions per endpoint |
| **Anti-Void Logic** | Cashier cannot void a sale without manager/admin approval |
| **Blind Stocktaking** | Cashier counts stock without seeing system quantities |
| **Audit Logs** | Every sensitive action logged with user, timestamp, and device |
| **Demand Forecasting** | 7-day rolling average with stock-out ETA alerts |
| **Trend Analysis** | Fast movers vs slow movers over configurable periods |
| **Multi-Branch** | Full branch isolation; owner sees consolidated dashboard |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.11 + Django 5 + DRF |
| Database (prod) | PostgreSQL (Render managed) |
| Database (local) | SQLite (zero config) |
| Auth | Token auth + django-otp (TOTP 2FA for admin) |
| Hosting | Render (Web Service + PostgreSQL) |
| Static files | Whitenoise |

---

## Local Development

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/omni-guard.git
cd omni-guard

# 2. Virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment variables
cp .env.example .env
# Edit .env if needed (defaults work for local dev)

# 5. Database setup
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

API available at: `http://127.0.0.1:8000/`  
Admin panel: `http://127.0.0.1:8000/admin/`

---

## API Endpoints

### Authentication
| Method | URL | Access |
|---|---|---|
| POST | `/api/auth/login/` | Public |
| POST | `/api/auth/register/` | Admin |
| POST | `/api/auth/logout/` | Authenticated |
| GET/PATCH | `/api/auth/me/` | Authenticated |

### Inventory
| Method | URL | Access |
|---|---|---|
| GET | `/api/inventory/products/` | All roles |
| POST | `/api/inventory/products/` | Manager+ |
| PATCH | `/api/inventory/products/{id}/` | Manager+ (margin: Admin only) |
| GET | `/api/inventory/products/low_stock/` | Manager+ |
| POST | `/api/inventory/movements/` | Manager+ |
| POST | `/api/inventory/stocktakes/` | All roles |
| POST | `/api/inventory/stocktakes/{id}/reconcile/` | Manager+ |

### Sales
| Method | URL | Access |
|---|---|---|
| POST | `/api/sales/` | All roles |
| GET | `/api/sales/` | Manager sees all; Cashier sees own |
| POST | `/api/sales/{id}/void/` | Manager+ |

### Analytics
| Method | URL | Access |
|---|---|---|
| GET | `/api/analytics/dashboard/` | All roles |
| GET | `/api/analytics/forecast/?days=7&lookahead=7` | Manager+ |
| GET | `/api/analytics/trends/?days=30` | Manager+ |

---

## Deploy to Render

### Option A — Automatic (render.yaml)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your GitHub repo — Render reads `render.yaml` and creates the web service + PostgreSQL automatically.
4. Set `DJANGO_SUPERUSER_PASSWORD` in the Render dashboard (Environment → Secret).
5. Click **Deploy**.

### Option B — Manual

1. **New Web Service** → connect GitHub repo.
2. Set:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
   - **Python version:** 3.11
3. **New PostgreSQL** → copy the Internal Database URL.
4. Add Environment Variables:
   ```
   DJANGO_SETTINGS_MODULE = backend.settings
   DEBUG = False
   SECRET_KEY = <generate a random string>
   DATABASE_URL = <paste from PostgreSQL>
   DJANGO_SUPERUSER_PASSWORD = <your secure password>
   ```
5. Deploy.

---

## Project Structure

```
omni-guard/
├── backend/
│   ├── settings.py          # Main Django settings
│   ├── urls.py              # Root URL router
│   ├── wsgi.py
│   ├── core/                # Branch model + AuditLog
│   ├── users/               # Custom User model + auth endpoints
│   ├── inventory/           # Products, StockMovements, Stocktaking
│   ├── sales/               # Sales, SaleItems, Anti-Void
│   └── analytics/           # Dashboard, Forecasting, Trends
├── requirements.txt
├── manage.py
├── build.sh                 # Render build script
├── render.yaml              # Infrastructure as code
├── .env.example
└── README.md
```

---

## Next Steps (Roadmap)

- [ ] Flutter mobile dashboard (owner view)
- [ ] PyQt offline POS client with SQLite sync
- [ ] M-Pesa payment integration
- [ ] SMS stock-out alerts (Africa's Talking)
- [ ] Multi-currency support

---

*Omni-Guard POS © 2026 — Built for Tanzanian businesses*
