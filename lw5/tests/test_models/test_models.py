import pytest
from app.models import Address, Order, Product, User


class TestModels:
    """Tests for data models"""

    def test_user_model_creation(self):
        """Test user model creation"""
        user = User(
            name="Test User", email="test@example.com", description="Test description"
        )

        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.description == "Test description"

    def test_user_repr(self):
        """Test user string representation"""
        user = User(id=1, name="Test User", email="test@example.com")

        repr_str = repr(user)
        assert "User" in repr_str
        assert "id=1" in repr_str
        assert "name='Test User'" in repr_str
        assert "email='test@example.com'" in repr_str

    def test_address_model_creation(self):
        """Test address model creation"""
        address = Address(street="Test Street", city="Test City", postal_code="12345")

        assert address.street == "Test Street"
        assert address.city == "Test City"
        assert address.postal_code == "12345"

    def test_address_repr(self):
        """Test address string representation"""
        address = Address(
            id=1, street="Test Street", city="Test City", postal_code="12345"
        )

        repr_str = repr(address)
        assert "Address" in repr_str
        assert "id=1" in repr_str
        assert "street='Test Street'" in repr_str

    def test_product_model_creation(self):
        """Test product model creation"""
        product = Product(
            name="Test Product",
            price=99.99,
            description="Test product description",
            stock_quantity=100,
        )

        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.description == "Test product description"
        assert product.stock_quantity == 100

    def test_order_model_creation(self):
        """Test order model creation"""
        order = Order(total_amount=199.98, status="pending")

        assert order.total_amount == 199.98
        assert order.status == "pending"
