"""
Django admin configuration for trading models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Stock, Portfolio, Transaction, Watchlist


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'balance', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'avatar')}),
        ('Trading Info', {'fields': ('balance',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'current_price', 'day_change_percent', 'sector', 'is_active')
    list_filter = ('is_active', 'sector')
    search_fields = ('symbol', 'name')
    ordering = ('symbol',)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'quantity', 'average_price', 'last_updated')
    list_filter = ('user', 'stock')
    search_fields = ('user__email', 'stock__symbol')
    ordering = ('-last_updated',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'transaction_type', 'quantity', 'price', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('user__email', 'stock__symbol')
    ordering = ('-timestamp',)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__email', 'stock__symbol')
    ordering = ('-added_at',)
