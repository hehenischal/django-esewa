import unittest
from unittest.mock import patch, MagicMock
from django.conf import settings
if not settings.configured:
    settings.configure()
from esewa.payment import EsewaPayment

class TestEsewaPayment(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        # Default test values
        self.test_product_code = "EPAYTEST"
        self.test_success_url = "http://test.com/success"
        self.test_failure_url = "http://test.com/failure"
        self.test_secret_key = "test_secret_key"
        self.test_amount = 1000.0
        self.test_uuid = "test-uuid-123"

    def test_initialization_default_values(self):
        """Test EsewaPayment initialization with default values."""
        payment = EsewaPayment()
        
        # Check default values
        self.assertEqual(payment.product_code, "EPAYTEST")
        self.assertEqual(payment.success_url, "http://localhost:8000/success/")
        self.assertEqual(payment.failure_url, "http://localhost:8000/failure/")
        self.assertEqual(payment.secret_key, "8gBm/:&EnhH.1/q")

    def test_initialization_custom_values(self):
        """Test EsewaPayment initialization with custom values."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            success_url=self.test_success_url,
            failure_url=self.test_failure_url,
            secret_key=self.test_secret_key
        )
        
        # Check custom values are set correctly
        self.assertEqual(payment.product_code, self.test_product_code)
        self.assertEqual(payment.success_url, self.test_success_url)
        self.assertEqual(payment.failure_url, self.test_failure_url)
        self.assertEqual(payment.secret_key, self.test_secret_key)

if __name__ == '__main__':
    unittest.main() 