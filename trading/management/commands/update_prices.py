"""
Management command to simulate stock price fluctuations.
Run this in a separate terminal: python manage.py update_prices
"""

import random
import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from trading.models import Stock


class Command(BaseCommand):
    help = 'Simulates real-time stock price fluctuations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=10,
            help='Update interval in seconds (default: 10)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        
        self.stdout.write(self.style.SUCCESS('🚀 Starting price updater...'))
        self.stdout.write(f'⏱️  Update interval: {interval} seconds')
        self.stdout.write(f'📊 Stocks to update: {Stock.objects.filter(is_active=True).count()}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Press Ctrl+C to stop'))
        self.stdout.write('=' * 60)
        
        update_count = 0
        
        try:
            while True:
                update_count += 1
                self.stdout.write(f'\n🔄 Update #{update_count} - {timezone.now().strftime("%H:%M:%S")}')
                
                stocks = Stock.objects.filter(is_active=True)
                updated = 0
                
                for stock in stocks:
                    old_price = stock.current_price
                    
                    # Random price change between -2% to +2%
                    change_percent = Decimal(random.uniform(-2.0, 2.0))
                    change_amount = old_price * (change_percent / 100)
                    new_price = old_price + change_amount
                    
                    # Ensure price doesn't go below ₹1
                    if new_price < 1:
                        new_price = Decimal('1.00')
                    
                    # Update stock
                    stock.current_price = round(new_price, 2)
                    stock.day_change = round(new_price - old_price, 2)
                    stock.day_change_percent = round(change_percent, 2)
                    stock.save()
                    
                    updated += 1
                    
                    # Show sample updates (first 5 stocks)
                    if updated <= 5:
                        symbol = f"{stock.symbol:12}"
                        arrow = "🟢" if change_percent >= 0 else "🔴"
                        sign = "+" if change_percent >= 0 else ""
                        self.stdout.write(
                            f"  {arrow} {symbol} ₹{old_price:8,.2f} → ₹{new_price:8,.2f} "
                            f"({sign}{change_percent:.2f}%)"
                        )
                
                self.stdout.write(self.style.SUCCESS(f'✅ Updated {updated} stocks'))
                
                # Wait before next update
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write('')
            self.stdout.write('=' * 60)
            self.stdout.write(self.style.WARNING('⏹️  Price updater stopped'))
            self.stdout.write(self.style.SUCCESS(f'📊 Total updates performed: {update_count}'))
