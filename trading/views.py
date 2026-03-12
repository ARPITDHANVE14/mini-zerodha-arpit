"""
Trading app views - renders HTML pages.
"""
from django.shortcuts import render


def home(request):
    """Home/landing page."""
    return render(request, 'trading/login.html')


def login_page(request):
    """Login page."""
    return render(request, 'trading/login.html')


def register_page(request):
    """Registration page."""
    return render(request, 'trading/register.html')


def dashboard(request):
    """Main dashboard."""
    return render(request, 'trading/dashboard.html')


def stocks(request):
    """Stocks listing page."""
    return render(request, 'trading/stocks.html')


def portfolio(request):
    """Portfolio page."""
    return render(request, 'trading/portfolio.html')


def transactions(request):
    """Transactions history page."""
    return render(request, 'trading/transactions.html')
