# 📈 Mini Zerodha - Paper Trading Platform

A full-stack paper trading platform built with Django and vanilla JavaScript.

##  Features

-  User authentication (email/password)
-  Virtual trading with ₹1,00,000 starting balance
-  Live price fluctuations (simulated)
-  Real-time dashboard with charts
-  Portfolio management
-  Transaction history
-  Stock search
-  Dark theme UI

##  Tech Stack

- **Backend:** Django 4.2, PostgreSQL
- **Frontend:** Vanilla JavaScript, CSS3
- **API:** Django REST Framework
- **Charts:** Chart.js

##  Setup

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mini-zerodha.git
cd mini-zerodha
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure database
```bash
cp .env.example .env
# Edit .env and set your PostgreSQL password
```

5. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_stocks
```

6. Start servers (need 2 terminals)
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
python manage.py update_prices


