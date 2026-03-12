from django.core.management.base import BaseCommand
from trading.models import Stock

class Command(BaseCommand):
    help = 'Seed the database with Indian stock data'

    def handle(self, *args, **kwargs):
        stocks_data = [
            {'symbol': 'RELIANCE', 'name': 'Reliance Industries Ltd.', 'current_price': 2456.75, 'sector': 'Energy'},
            {'symbol': 'TCS', 'name': 'Tata Consultancy Services Ltd.', 'current_price': 3678.90, 'sector': 'IT'},
            {'symbol': 'HDFCBANK', 'name': 'HDFC Bank Ltd.', 'current_price': 1654.30, 'sector': 'Banking'},
            {'symbol': 'INFY', 'name': 'Infosys Ltd.', 'current_price': 1456.80, 'sector': 'IT'},
            {'symbol': 'ICICIBANK', 'name': 'ICICI Bank Ltd.', 'current_price': 987.45, 'sector': 'Banking'},
            {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever Ltd.', 'current_price': 2543.60, 'sector': 'FMCG'},
            {'symbol': 'ITC', 'name': 'ITC Ltd.', 'current_price': 456.75, 'sector': 'FMCG'},
            {'symbol': 'SBIN', 'name': 'State Bank of India', 'current_price': 623.90, 'sector': 'Banking'},
            {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel Ltd.', 'current_price': 1123.45, 'sector': 'Telecom'},
            {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank Ltd.', 'current_price': 1789.20, 'sector': 'Banking'},
            {'symbol': 'LT', 'name': 'Larsen & Toubro Ltd.', 'current_price': 3245.80, 'sector': 'Engineering'},
            {'symbol': 'AXISBANK', 'name': 'Axis Bank Ltd.', 'current_price': 1034.55, 'sector': 'Banking'},
            {'symbol': 'ASIANPAINT', 'name': 'Asian Paints Ltd.', 'current_price': 3123.90, 'sector': 'Consumer Goods'},
            {'symbol': 'MARUTI', 'name': 'Maruti Suzuki India Ltd.', 'current_price': 10234.50, 'sector': 'Automobile'},
            {'symbol': 'SUNPHARMA', 'name': 'Sun Pharmaceutical Industries Ltd.', 'current_price': 1156.75, 'sector': 'Pharma'},
            {'symbol': 'TITAN', 'name': 'Titan Company Ltd.', 'current_price': 3345.60, 'sector': 'Consumer Goods'},
            {'symbol': 'TATAMOTORS', 'name': 'Tata Motors Ltd.', 'current_price': 745.30, 'sector': 'Automobile'},
            {'symbol': 'NTPC', 'name': 'NTPC Ltd.', 'current_price': 234.55, 'sector': 'Energy'},
            {'symbol': 'POWERGRID', 'name': 'Power Grid Corporation of India Ltd.', 'current_price': 267.80, 'sector': 'Energy'},
            {'symbol': 'NESTLEIND', 'name': 'Nestle India Ltd.', 'current_price': 23456.90, 'sector': 'FMCG'},
            {'symbol': 'ULTRACEMCO', 'name': 'UltraTech Cement Ltd.', 'current_price': 8976.45, 'sector': 'Cement'},
            {'symbol': 'BAJFINANCE', 'name': 'Bajaj Finance Ltd.', 'current_price': 7234.80, 'sector': 'Finance'},
            {'symbol': 'WIPRO', 'name': 'Wipro Ltd.', 'current_price': 456.90, 'sector': 'IT'},
            {'symbol': 'ONGC', 'name': 'Oil and Natural Gas Corporation Ltd.', 'current_price': 189.75, 'sector': 'Energy'},
            {'symbol': 'ADANIPORTS', 'name': 'Adani Ports and Special Economic Zone Ltd.', 'current_price': 1234.60, 'sector': 'Infrastructure'},
            {'symbol': 'TATASTEEL', 'name': 'Tata Steel Ltd.', 'current_price': 145.90, 'sector': 'Steel'},
            {'symbol': 'TECHM', 'name': 'Tech Mahindra Ltd.', 'current_price': 1345.75, 'sector': 'IT'},
            {'symbol': 'HCLTECH', 'name': 'HCL Technologies Ltd.', 'current_price': 1567.80, 'sector': 'IT'},
            {'symbol': 'BAJAJFINSV', 'name': 'Bajaj Finserv Ltd.', 'current_price': 1678.90, 'sector': 'Finance'},
            {'symbol': 'DRREDDY', 'name': 'Dr. Reddy\'s Laboratories Ltd.', 'current_price': 5678.45, 'sector': 'Pharma'},
            {'symbol': 'GRASIM', 'name': 'Grasim Industries Ltd.', 'current_price': 1934.70, 'sector': 'Cement'},
            {'symbol': 'M&M', 'name': 'Mahindra & Mahindra Ltd.', 'current_price': 1845.60, 'sector': 'Automobile'},
            {'symbol': 'DIVISLAB', 'name': 'Divi\'s Laboratories Ltd.', 'current_price': 3567.90, 'sector': 'Pharma'},
            {'symbol': 'CIPLA', 'name': 'Cipla Ltd.', 'current_price': 1234.55, 'sector': 'Pharma'},
            {'symbol': 'EICHERMOT', 'name': 'Eicher Motors Ltd.', 'current_price': 3876.40, 'sector': 'Automobile'},
            {'symbol': 'BPCL', 'name': 'Bharat Petroleum Corporation Ltd.', 'current_price': 378.90, 'sector': 'Energy'},
            {'symbol': 'INDUSINDBK', 'name': 'IndusInd Bank Ltd.', 'current_price': 1456.75, 'sector': 'Banking'},
            {'symbol': 'COALINDIA', 'name': 'Coal India Ltd.', 'current_price': 267.85, 'sector': 'Mining'},
            {'symbol': 'HEROMOTOCO', 'name': 'Hero MotoCorp Ltd.', 'current_price': 3245.90, 'sector': 'Automobile'},
            {'symbol': 'BRITANNIA', 'name': 'Britannia Industries Ltd.', 'current_price': 4876.50, 'sector': 'FMCG'},
            {'symbol': 'JSWSTEEL', 'name': 'JSW Steel Ltd.', 'current_price': 789.65, 'sector': 'Steel'},
            {'symbol': 'SHREECEM', 'name': 'Shree Cement Ltd.', 'current_price': 27456.80, 'sector': 'Cement'},
            {'symbol': 'HINDALCO', 'name': 'Hindalco Industries Ltd.', 'current_price': 567.90, 'sector': 'Metal'},
            {'symbol': 'ADANIENT', 'name': 'Adani Enterprises Ltd.', 'current_price': 2345.75, 'sector': 'Infrastructure'},
            {'symbol': 'APOLLOHOSP', 'name': 'Apollo Hospitals Enterprise Ltd.', 'current_price': 5678.90, 'sector': 'Healthcare'},
            {'symbol': 'TATACONSUM', 'name': 'Tata Consumer Products Ltd.', 'current_price': 1023.45, 'sector': 'FMCG'},
            {'symbol': 'SBILIFE', 'name': 'SBI Life Insurance Company Ltd.', 'current_price': 1456.80, 'sector': 'Finance'},
            {'symbol': 'BAJAJ-AUTO', 'name': 'Bajaj Auto Ltd.', 'current_price': 8976.55, 'sector': 'Automobile'},
            {'symbol': 'HDFCLIFE', 'name': 'HDFC Life Insurance Company Ltd.', 'current_price': 678.90, 'sector': 'Finance'},
            {'symbol': 'UPL', 'name': 'UPL Ltd.', 'current_price': 567.85, 'sector': 'Chemicals'},
        ]

        self.stdout.write('Seeding 50 stocks...')
        
        created_count = 0
        updated_count = 0
        
        for data in stocks_data:
            stock, created = Stock.objects.update_or_create(
                symbol=data['symbol'],
                defaults={
                    'name': data['name'],
                    'current_price': data['current_price'],
                    'sector': data['sector'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created: {stock.symbol} - {stock.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'📝 Updated: {stock.symbol} - {stock.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully seeded stocks!'))
        self.stdout.write(f'   - Created: {created_count}')
        self.stdout.write(f'   - Updated: {updated_count}')
        self.stdout.write(f'   - Total: {created_count + updated_count}')
