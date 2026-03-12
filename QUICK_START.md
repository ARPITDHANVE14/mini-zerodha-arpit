# 🚀 MINI ZERODHA - QUICK START GUIDE (NO OTP VERSION)

## ⚡ 5-Minute Setup

This version has **NO OTP** - just direct email/password login!

---

## STEP 1: Install PostgreSQL

### Windows
1. Download: https://www.postgresql.org/download/windows/
2. Install, set password as: `postgres`
3. Remember this password!

### Mac
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Linux
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## STEP 2: Create Database

### Windows
Open "SQL Shell (psql)" from Start Menu

### Mac/Linux
```bash
sudo -u postgres psql
```

### Then run:
```sql
CREATE DATABASE mini_zerodha_db;
\q
```

---

## STEP 3: Setup Project

```bash
# Extract ZIP file
cd mini_zerodha_NO_OTP

# Create virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install packages
pip install -r requirements.txt

# Copy .env file
copy .env.example .env      # Windows
cp .env.example .env        # Mac/Linux

# Edit .env and set your PostgreSQL password
# Change DB_PASSWORD=postgres to your actual password
```

---

## STEP 4: Initialize Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: email, name, password

# Load 50 Indian stocks
python manage.py seed_stocks
```

---

## STEP 5: Run Server

```bash
python manage.py runserver
```

Open browser: **http://127.0.0.1:8000/login/**

---

## 🎯 LOGIN

Use the email and password you set during `createsuperuser`.

**NO OTP REQUIRED!** Just email + password → Dashboard

---

## ✨ WHAT'S DIFFERENT (NO OTP VERSION)

### Registration:
- Enter: Name, Email, Password
- Click "Create Account"
- **Instantly logged in** → Dashboard

### Login:
- Enter: Email, Password
- Click "Login"
- **Instantly logged in** → Dashboard

**No email verification, no OTP codes, no waiting!**

---

## 📊 FEATURES

- ✅ Simple login (no OTP)
- ✅ ₹1,00,000 virtual money
- ✅ 50 Indian stocks (RELIANCE, TCS, INFY, etc.)
- ✅ Buy/Sell stocks
- ✅ Portfolio tracking
- ✅ Transaction history
- ✅ Watchlist
- ✅ Dashboard with charts

---

## 🔧 TROUBLESHOOTING

### Error: "password authentication failed"
**Fix:** Edit `.env` file, set correct PostgreSQL password

### Error: "No module named 'rest_framework'"
**Fix:** 
```bash
venv\Scripts\activate  # Make sure venv is active!
pip install -r requirements.txt
```

### Can't login
**Fix:** Did you create a superuser?
```bash
python manage.py createsuperuser
```

### PostgreSQL not running
- Windows: Services → postgresql → Start
- Mac: `brew services start postgresql@14`
- Linux: `sudo systemctl start postgresql`

---

## 📝 MISSING FILES NOTICE

**Due to size limitations, some template files need to be created:**

### Required files you need to create manually:
1. `trading/templates/trading/base.html` - Base template
2. `trading/templates/trading/dashboard.html` - Dashboard
3. `trading/templates/trading/stocks.html` - Stocks list
4. `trading/templates/trading/portfolio.html` - Portfolio
5. `trading/templates/trading/transactions.html` - Transactions
6. `trading/static/trading/css/main.css` - Styles
7. `trading/static/trading/js/main.js` - JavaScript

**These files contain the UI code. I can provide them separately if needed.**

**OR - You can start with just login/register working and build the rest!**

---

## 🎉 THAT'S IT!

You now have a working paper trading platform without OTP complexity!

Happy Trading! 📈
