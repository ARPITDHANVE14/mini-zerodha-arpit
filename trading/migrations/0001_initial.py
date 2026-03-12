# Generated initial migration for trading app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=100000.00, help_text='Available cash balance in INR', max_digits=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(help_text='Stock ticker symbol', max_length=20, unique=True)),
                ('name', models.CharField(help_text='Company name', max_length=200)),
                ('sector', models.CharField(blank=True, max_length=100)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_change', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('day_change_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('volume', models.BigIntegerField(default=0)),
                ('market_cap', models.BigIntegerField(default=0, help_text='Market cap in crores')),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'stocks',
                'ordering': ['symbol'],
            },
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'watchlist',
                'ordering': ['-added_at'],
                'unique_together': {('user', 'stock')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'transactions',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('average_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'portfolio',
                'unique_together': {('user', 'stock')},
            },
        ),
    ]
