"""
Mini Zerodha - Django Models (NO OTP VERSION)
Simplified models with direct email/password authentication.
"""

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# ═══════════════════════════════════════════════════════════════════
# CUSTOM USER MANAGER
# ═══════════════════════════════════════════════════════════════════
class UserManager(BaseUserManager):
    """Custom manager for email-based authentication."""

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


# ═══════════════════════════════════════════════════════════════════
# USER MODEL
# ═══════════════════════════════════════════════════════════════════
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email-based authentication.
    Each user starts with ₹1,00,000 demo balance for paper trading.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2,
        default=Decimal('100000.00'),
        help_text="Available cash balance in INR"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def total_investment(self):
        """Calculate total money invested in current holdings."""
        return sum(
            h.quantity * h.average_price
            for h in self.portfolio.all()
        )

    @property
    def total_value(self):
        """Calculate total portfolio value at current prices."""
        return sum(
            h.quantity * h.stock.current_price
            for h in self.portfolio.all()
        )

    @property
    def profit_loss(self):
        """Calculate total profit/loss."""
        return self.total_value - self.total_investment

    @property
    def total_assets(self):
        """Total assets = cash balance + portfolio value."""
        return self.balance + self.total_value


# ═══════════════════════════════════════════════════════════════════
# STOCK MODEL
# ═══════════════════════════════════════════════════════════════════
class Stock(models.Model):
    """
    Represents a tradable stock/security.
    Prices are simulated for demo purposes.
    """
    symbol = models.CharField(max_length=20, unique=True, help_text="Stock ticker symbol")
    name = models.CharField(max_length=200, help_text="Company name")
    sector = models.CharField(max_length=100, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    day_change = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    day_change_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    volume = models.BigIntegerField(default=0)
    market_cap = models.BigIntegerField(default=0, help_text="Market cap in crores")
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stocks'
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


# ═══════════════════════════════════════════════════════════════════
# PORTFOLIO MODEL
# ═══════════════════════════════════════════════════════════════════
class Portfolio(models.Model):
    """
    User's stock holdings.
    Tracks quantity and average purchase price.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='portfolio')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio'
        unique_together = ('user', 'stock')

    def __str__(self):
        return f"{self.user.email} - {self.stock.symbol} ({self.quantity})"

    @property
    def invested_amount(self):
        """Total amount invested in this holding."""
        return self.quantity * self.average_price

    @property
    def current_value(self):
        """Current market value of this holding."""
        return self.quantity * self.stock.current_price

    @property
    def profit_loss(self):
        """Profit/loss for this holding."""
        return self.current_value - self.invested_amount

    @property
    def profit_loss_percent(self):
        """Profit/loss percentage for this holding."""
        if self.invested_amount == 0:
            return 0
        return (self.profit_loss / self.invested_amount) * 100


# ═══════════════════════════════════════════════════════════════════
# TRANSACTION MODEL
# ═══════════════════════════════════════════════════════════════════
class Transaction(models.Model):
    """
    Records all buy/sell transactions.
    """
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='transactions')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transactions'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} {self.quantity} {self.stock.symbol}"


# ═══════════════════════════════════════════════════════════════════
# WATCHLIST MODEL
# ═══════════════════════════════════════════════════════════════════
class Watchlist(models.Model):
    """
    User's watchlist for monitoring stocks.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'watchlist'
        unique_together = ('user', 'stock')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email} - {self.stock.symbol}"
