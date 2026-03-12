# 🚀 COMPLETE SETUP GUIDE

## ✨ What's Included (100% Complete)

### ✅ Backend
- Django 4.2 with PostgreSQL
- User authentication (no OTP)
- All API endpoints working
- Admin panel configured

### ✅ Frontend  
- Login & Register pages
- Dashboard with live charts
- Stocks listing (search & buy)
- Portfolio management (sell stocks)
- Transaction history
- Live price updates every 10 seconds

### ✅ Price Simulation
- Background script that updates stock prices
- Realistic ±2% fluctuations
- Updates every 10 seconds
- Shows green/red price changes

---

## 📥 STEP-BY-STEP SETUP

### 1. Install PostgreSQL

**Windows:**
```
Download from: https://www.postgresql.org/download/windows/
Install with password: postgres
```

**Mac:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

```bash
# Windows: Open "SQL Shell (psql)"
# Mac/Linux: sudo -u postgres psql

CREATE DATABASE mini_zerodha_db;
\q
```

### 3. Setup Project

```bash
cd mini_zerodha_FINAL

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install packages
pip install -r requirements.txt
```

### 4. Configure Database

```bash
# Copy .env file
copy .env.example .env      # Windows
cp .env.example .env        # Mac/Linux

# Edit .env and set:
DB_PASSWORD=your_postgres_password
```

### 5. Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_stocks
```

### 6. Run the Application

You need **TWO terminals**:

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Price Updater:**
```bash
python manage.py update_prices
```

### 7. Open Browser

```
http://127.0.0.1:8000/login/
```

Login with the credentials you set in `createsuperuser`.

---

## 🎯 HOW IT WORKS

### Price Fluctuations
- Terminal 2 updates stock prices every 10 seconds
- Prices change by ±0.5% to ±3% randomly
- Frontend auto-refreshes to show new prices
- Green = price up, Red = price down

### Trading
1. Browse stocks on Stocks page
2. Click "Buy" → Enter quantity → Confirm
3. View holdings in Portfolio
4. Click "Sell" → Enter quantity → Confirm
5. All transactions appear in Transactions page

### Dashboard
- Shows your total balance, investments, P&L
- Portfolio distribution pie chart
- Top gainers list (updates live)
- Recent stocks with live prices

---

## ⚙️ OPTIONAL: Customize Price Update Interval

Default is 10 seconds. To change:

```bash
# Update every 5 seconds (faster)
python manage.py update_prices --interval 5

# Update every 30 seconds (slower)
python manage.py update_prices --interval 30
```

---

## 🐛 TROUBLESHOOTING

### Error: "password authentication failed"
**Fix:** Edit `.env` file, set correct PostgreSQL password

### Prices not updating
**Fix:** Make sure Terminal 2 is running `update_prices` command

### Can't login
**Fix:** Did you run `createsuperuser`?

### "No module named 'rest_framework'"
**Fix:** Activate venv, then `pip install -r requirements.txt`

---

## 📊 FEATURES

- ✅ User registration & login (no OTP)
- ✅ ₹1,00,000 starting balance
- ✅ 50 Indian stocks (NSE)
- ✅ Live price updates (every 10s)
- ✅ Buy/Sell stocks
- ✅ Portfolio tracking with P&L
- ✅ Transaction history
- ✅ Dashboard with charts
- ✅ Search stocks
- ✅ Responsive design

---

## 🎉 YOU'RE READY!

1. Start Django server (Terminal 1)
2. Start price updater (Terminal 2)
3. Open http://127.0.0.1:8000/login/
4. Login and start trading!

**Watch prices change in real-time!** 📈📉

---

## 💡 TIPS

- Keep both terminals running
- Prices update every 10 seconds
- Dashboard auto-refreshes
- All data is saved in PostgreSQL
- Use Django Admin: http://127.0.0.1:8000/admin/
