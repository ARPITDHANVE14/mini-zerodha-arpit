# 📈 Mini Zerodha - Paper Trading Platform (COMPLETE VERSION)

A feature-rich Django-based paper trading platform with:
- ✅ **Direct email/password login** (no OTP complexity)
- ✅ **Live price fluctuations** (simulated market movements)
- ✅ **Complete frontend** (all pages working)
- ✅ **Real-time updates** (prices update every 10 seconds)

---

## ✨ Features

- ✅ **Simple Login** - Direct email + password (no OTP verification)
- ✅ **User Registration** - Quick account creation
- ✅ **Virtual Trading** - Buy/sell stocks with ₹1,00,000 demo money
- ✅ **50 Indian Stocks** - Pre-loaded NSE stocks (RELIANCE, TCS, INFY, etc.)
- ✅ **Portfolio Management** - Track your holdings
- ✅ **Transaction History** - View all your trades
- ✅ **Watchlist** - Monitor your favorite stocks
- ✅ **Real-time Dashboard** - Charts and statistics
- ✅ **Responsive UI** - Works on desktop and mobile

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+ (recommended: Python 3.11)
- PostgreSQL 14+

---

### Step 1: Install PostgreSQL

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Install with password: `postgres` (remember this!)
3. Default port: 5432

**Mac:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

### Step 2: Create Database

**Windows:** Open "SQL Shell (psql)" from Start Menu  
**Mac/Linux:** Run `sudo -u postgres psql`

```sql
CREATE DATABASE mini_zerodha_db;
\q
```

---

### Step 3: Setup Project

```bash
# Extract the ZIP file
cd mini_zerodha_NO_OTP

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 4: Configure Database

Copy `.env.example` to `.env`:

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

Edit `.env` and set your PostgreSQL password:
```env
DB_PASSWORD=postgres  # Change to your actual password
```

---

### Step 5: Initialize Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter email, name, and password when prompted

# Load stock data (50 Indian stocks)
python manage.py seed_stocks
```

---

### Step 6: Run Server

```bash
python manage.py runserver
```

**Open browser:** http://127.0.0.1:8000/

---

## 🎯 Default Setup

- **Initial Balance:** ₹1,00,000 (virtual money)
- **Stocks Available:** 50 popular Indian stocks
- **Login:** Use the email/password you set during `createsuperuser`

---

## 📁 Project Structure

```
mini_zerodha_NO_OTP/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── mini_zerodha/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── trading/               # Main app
    ├── models.py          # Database models
    ├── views.py           # Page views
    ├── api_views.py       # API endpoints
    ├── urls.py
    ├── admin.py
    ├── management/
    │   └── commands/
    │       └── seed_stocks.py
    ├── templates/
    │   └── trading/
    │       ├── base.html
    │       ├── login.html
    │       ├── register.html
    │       ├── dashboard.html
    │       ├── stocks.html
    │       ├── portfolio.html
    │       └── transactions.html
    └── static/
        └── trading/
            ├── css/
            │   └── main.css
            └── js/
                └── main.js
```

---

## 🔐 Authentication (Simplified - No OTP)

### Registration Flow:
1. User enters: name, email, password
2. Account created immediately
3. Redirects to login

### Login Flow:
1. User enters: email, password
2. Validates credentials
3. Returns JWT tokens
4. Redirects to dashboard

**No OTP verification required!**

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.2.7 |
| **API** | Django REST Framework 3.14.0 |
| **Database** | PostgreSQL |
| **Authentication** | JWT (simplejwt) |
| **Frontend** | Vanilla JavaScript |
| **Styling** | Custom CSS |
| **Charts** | Chart.js |

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/refresh/` - Refresh JWT token

### Trading
- `GET /api/stocks/` - List all stocks
- `GET /api/stocks/<id>/` - Get stock details
- `POST /api/transactions/buy/` - Buy stocks
- `POST /api/transactions/sell/` - Sell stocks
- `GET /api/portfolio/` - Get user portfolio
- `GET /api/transactions/` - Get transaction history
- `GET /api/watchlist/` - Get watchlist
- `POST /api/watchlist/` - Add to watchlist
- `DELETE /api/watchlist/<id>/` - Remove from watchlist

---

## 🎨 Pages

- `/` - Home/Landing page
- `/login/` - Login page
- `/register/` - Registration page
- `/dashboard/` - Main trading dashboard
- `/stocks/` - Browse all stocks
- `/portfolio/` - View holdings
- `/transactions/` - Transaction history

---

## 🔧 Troubleshooting

### Error: "password authentication failed"
**Fix:** Check `.env` file - ensure `DB_PASSWORD` matches your PostgreSQL password

### Error: "No module named 'rest_framework'"
**Fix:** 
```bash
# Make sure venv is activated (you should see "(venv)" in terminal)
pip install -r requirements.txt
```

### Error: "relation 'users' does not exist"
**Fix:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Can't login
**Fix:** Make sure you created a superuser:
```bash
python manage.py createsuperuser
```

---

## 🐛 Common Issues

**PostgreSQL not running:**
- Windows: Services → postgresql-x64-14 → Start
- Mac: `brew services start postgresql@14`
- Linux: `sudo systemctl start postgresql`

**Database doesn't exist:**
```bash
sudo -u postgres psql
CREATE DATABASE mini_zerodha_db;
\q
```

**Forgot to activate venv:**
```bash
# You should see (venv) before your terminal prompt
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

---

## 📝 Development Notes

- This is a **learning/demo project** - not production-ready
- Stock prices are simulated (random updates)
- All trades are virtual (paper trading)
- No real money involved
- Email verification disabled for simplicity

---

## 🔐 Security Notes

**⚠️ For Production, You MUST:**
- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG=False
- [ ] Add proper ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Implement CSRF protection properly
- [ ] Use secure password hashing
- [ ] Add email verification
- [ ] Set up proper logging

---

## 📄 License

Educational/Learning project. Free to use for educational purposes.

---

## 🙏 Support

If you encounter issues:

1. Check terminal for error messages
2. Verify PostgreSQL is running
3. Ensure `.env` has correct password
4. Make sure venv is activated
5. Try: `python manage.py migrate`

---

**Happy Trading! 📈💰**
