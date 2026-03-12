"""
Trading app URL configuration.
"""
from django.urls import path
from . import views, api_views

urlpatterns = [
    # Page views
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stocks/', views.stocks, name='stocks'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('transactions/', views.transactions, name='transactions'),

    # API endpoints - Authentication
    path('api/auth/register/', api_views.RegisterView.as_view(), name='api_register'),
    path('api/auth/login/', api_views.LoginView.as_view(), name='api_login'),
    path('api/auth/me/', api_views.CurrentUserView.as_view(), name='api_me'),

    # API endpoints - Stocks
    path('api/stocks/', api_views.StockListView.as_view(), name='api_stocks'),
    path('api/stocks/<int:pk>/', api_views.StockDetailView.as_view(), name='api_stock_detail'),

    # API endpoints - Trading
    path('api/transactions/buy/', api_views.BuyStockView.as_view(), name='api_buy'),
    path('api/transactions/sell/', api_views.SellStockView.as_view(), name='api_sell'),

    # API endpoints - Portfolio & Transactions
    path('api/portfolio/', api_views.PortfolioView.as_view(), name='api_portfolio'),
    path('api/transactions/', api_views.TransactionListView.as_view(), name='api_transactions'),

    # API endpoints - Watchlist
    path('api/watchlist/', api_views.WatchlistView.as_view(), name='api_watchlist'),
    path('api/watchlist/<int:pk>/', api_views.WatchlistDeleteView.as_view(), name='api_watchlist_delete'),
]
