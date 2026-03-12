"""
Mini Zerodha - API Views (NO OTP VERSION)
Simplified authentication with direct email/password login.
"""

from decimal import Decimal
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction as db_transaction
from .models import User, Stock, Portfolio, Transaction, Watchlist
from rest_framework import serializers


# ═══════════════════════════════════════════════════════════════════
# SERIALIZERS
# ═══════════════════════════════════════════════════════════════════

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'balance', 'date_joined']
        read_only_fields = ['id', 'balance', 'date_joined']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    invested_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    current_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    profit_loss_percent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class WatchlistSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = '__all__'


# ═══════════════════════════════════════════════════════════════════
# AUTHENTICATION VIEWS (NO OTP)
# ═══════════════════════════════════════════════════════════════════

class RegisterView(APIView):
    """
    Register a new user - NO OTP required.
    Creates account immediately.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        name = request.data.get('name', '').strip()
        password = request.data.get('password', '')

        # Validation
        if not all([email, name, password]):
            return Response(
                {'error': 'Email, name, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user immediately (no OTP)
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Registration successful!',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Login with email and password - NO OTP required.
    Returns JWT tokens immediately.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful!',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })


class CurrentUserView(APIView):
    """
    Get current authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ═══════════════════════════════════════════════════════════════════
# STOCK VIEWS
# ═══════════════════════════════════════════════════════════════════

class StockListView(generics.ListAPIView):
    """List all active stocks."""
    queryset = Stock.objects.filter(is_active=True)
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]


class StockDetailView(generics.RetrieveAPIView):
    """Get details of a specific stock."""
    queryset = Stock.objects.filter(is_active=True)
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]


# ═══════════════════════════════════════════════════════════════════
# TRADING VIEWS
# ═══════════════════════════════════════════════════════════════════

class BuyStockView(APIView):
    """Buy stocks."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stock_id = request.data.get('stock_id')
        quantity = request.data.get('quantity')

        # Validation
        if not stock_id or not quantity:
            return Response(
                {'error': 'stock_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            return Response(
                {'error': 'Quantity must be a positive integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get stock
        try:
            stock = Stock.objects.get(id=stock_id, is_active=True)
        except Stock.DoesNotExist:
            return Response(
                {'error': 'Stock not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        total_cost = stock.current_price * quantity

        # Check balance
        if user.balance < total_cost:
            return Response(
                {'error': f'Insufficient balance. Required: ₹{total_cost}, Available: ₹{user.balance}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Execute transaction
        with db_transaction.atomic():
            # Deduct balance
            user.balance -= total_cost
            user.save()

            # Update portfolio
            portfolio, created = Portfolio.objects.get_or_create(
                user=user,
                stock=stock,
                defaults={'quantity': 0, 'average_price': stock.current_price}
            )

            if created:
                portfolio.quantity = quantity
                portfolio.average_price = stock.current_price
            else:
                # Calculate new average price
                total_quantity = portfolio.quantity + quantity
                total_investment = (portfolio.quantity * portfolio.average_price) + (quantity * stock.current_price)
                portfolio.average_price = total_investment / total_quantity
                portfolio.quantity = total_quantity

            portfolio.save()

            # Record transaction
            transaction_obj = Transaction.objects.create(
                user=user,
                stock=stock,
                transaction_type='BUY',
                quantity=quantity,
                price=stock.current_price,
                total_amount=total_cost
            )

        return Response({
            'message': f'Successfully bought {quantity} shares of {stock.symbol}',
            'transaction': TransactionSerializer(transaction_obj).data,
            'new_balance': float(user.balance)
        })


class SellStockView(APIView):
    """Sell stocks."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stock_id = request.data.get('stock_id')
        quantity = request.data.get('quantity')

        # Validation
        if not stock_id or not quantity:
            return Response(
                {'error': 'stock_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            return Response(
                {'error': 'Quantity must be a positive integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get stock
        try:
            stock = Stock.objects.get(id=stock_id, is_active=True)
        except Stock.DoesNotExist:
            return Response(
                {'error': 'Stock not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        # Check holdings
        try:
            portfolio = Portfolio.objects.get(user=user, stock=stock)
        except Portfolio.DoesNotExist:
            return Response(
                {'error': 'You don\'t own this stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if portfolio.quantity < quantity:
            return Response(
                {'error': f'Insufficient holdings. You own {portfolio.quantity} shares'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_proceeds = stock.current_price * quantity

        # Execute transaction
        with db_transaction.atomic():
            # Add balance
            user.balance += total_proceeds
            user.save()

            # Update portfolio
            portfolio.quantity -= quantity
            if portfolio.quantity == 0:
                portfolio.delete()
            else:
                portfolio.save()

            # Record transaction
            transaction_obj = Transaction.objects.create(
                user=user,
                stock=stock,
                transaction_type='SELL',
                quantity=quantity,
                price=stock.current_price,
                total_amount=total_proceeds
            )

        return Response({
            'message': f'Successfully sold {quantity} shares of {stock.symbol}',
            'transaction': TransactionSerializer(transaction_obj).data,
            'new_balance': float(user.balance)
        })


# ═══════════════════════════════════════════════════════════════════
# PORTFOLIO & TRANSACTION VIEWS
# ═══════════════════════════════════════════════════════════════════

class PortfolioView(generics.ListAPIView):
    """Get user's portfolio."""
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class TransactionListView(generics.ListAPIView):
    """Get user's transaction history."""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# ═══════════════════════════════════════════════════════════════════
# WATCHLIST VIEWS
# ═══════════════════════════════════════════════════════════════════

class WatchlistView(generics.ListCreateAPIView):
    """Get or add to watchlist."""
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def post(self, request):
        stock_id = request.data.get('stock_id')

        try:
            stock = Stock.objects.get(id=stock_id, is_active=True)
        except Stock.DoesNotExist:
            return Response(
                {'error': 'Stock not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        watchlist, created = Watchlist.objects.get_or_create(
            user=request.user,
            stock=stock
        )

        if not created:
            return Response(
                {'error': 'Stock already in watchlist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            WatchlistSerializer(watchlist).data,
            status=status.HTTP_201_CREATED
        )


class WatchlistDeleteView(generics.DestroyAPIView):
    """Remove from watchlist."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
