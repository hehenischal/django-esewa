import unittest
from unittest.mock import patch, MagicMock
import json
import base64
import requests
from django_esewa.payment import EsewaPayment

class TestEsewaPayment(unittest.TestCase):
    def setUp(self):
        """Set up test cases with common test values."""
        self.test_product_code = "EPAYTEST"
        self.test_success_url = "http://test.com/success"
        self.test_failure_url = "http://test.com/failure"
        self.test_secret_key = "test_secret_key"
        self.test_amount = 1000.0
        self.test_tax_amount = 130.0
        self.test_total_amount = 1130.0
        self.test_service_charge = 50.0
        self.test_delivery_charge = 100.0
        self.test_uuid = "test-uuid-123"

    def test_initialization_default_values(self):
        """Test EsewaPayment initialization with default values."""
        payment = EsewaPayment()
        
        # Check default values
        self.assertEqual(payment.product_code, "EPAYTEST")
        self.assertEqual(payment.success_url, "http://localhost:8000/success/")
        self.assertEqual(payment.failure_url, "http://localhost:8000/failure/")
        self.assertEqual(payment.secret_key, "8gBm/:&EnhH.1/q")
        self.assertEqual(payment.amount, 0)
        self.assertEqual(payment.tax_amount, 0)
        self.assertEqual(payment.total_amount, 0)
        self.assertEqual(payment.product_service_charge, 0)
        self.assertEqual(payment.product_delivery_charge, 0)
        self.assertIsNone(payment.transaction_uuid)

    def test_initialization_custom_values(self):
        """Test EsewaPayment initialization with custom values."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            success_url=self.test_success_url,
            failure_url=self.test_failure_url,
            secret_key=self.test_secret_key,
            amount=self.test_amount,
            tax_amount=self.test_tax_amount,
            total_amount=self.test_total_amount,
            product_service_charge=self.test_service_charge,
            product_delivery_charge=self.test_delivery_charge,
            transaction_uuid=self.test_uuid
        )
        
        # Check all custom values are set correctly
        self.assertEqual(payment.product_code, self.test_product_code)
        self.assertEqual(payment.success_url, self.test_success_url)
        self.assertEqual(payment.failure_url, self.test_failure_url)
        self.assertEqual(payment.secret_key, self.test_secret_key)
        self.assertEqual(payment.amount, self.test_amount)
        self.assertEqual(payment.tax_amount, self.test_tax_amount)
        self.assertEqual(payment.total_amount, self.test_total_amount)
        self.assertEqual(payment.product_service_charge, self.test_service_charge)
        self.assertEqual(payment.product_delivery_charge, self.test_delivery_charge)
        self.assertEqual(payment.transaction_uuid, self.test_uuid)

    def test_create_signature_with_uuid(self):
        """Test signature creation with provided transaction UUID."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key,
            total_amount=self.test_total_amount
        )
        signature = payment.create_signature(self.test_uuid)
        self.assertIsNotNone(signature)
        self.assertEqual(payment.transaction_uuid, self.test_uuid)
        self.assertEqual(payment.signature, signature)

    def test_create_signature_without_uuid(self):
        """Test signature creation with UUID set in constructor."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        signature = payment.create_signature()
        self.assertIsNotNone(signature)
        self.assertEqual(payment.transaction_uuid, self.test_uuid)
        self.assertEqual(payment.signature, signature)

    def test_generate_form(self):
        """Test form generation with all fields."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            success_url=self.test_success_url,
            failure_url=self.test_failure_url,
            secret_key=self.test_secret_key,
            amount=self.test_amount,
            tax_amount=self.test_tax_amount,
            total_amount=self.test_total_amount,
            product_service_charge=self.test_service_charge,
            product_delivery_charge=self.test_delivery_charge,
            transaction_uuid=self.test_uuid
        )
        payment.create_signature()
        form = payment.generate_form()
        
        # Check if all required fields are in the form
        self.assertIn(f'name="amount" value="{self.test_amount}"', form)
        self.assertIn(f'name="product_delivery_charge" value="{self.test_delivery_charge}"', form)
        self.assertIn(f'name="product_service_charge" value="{self.test_service_charge}"', form)
        self.assertIn(f'name="total_amount" value="{self.test_total_amount}"', form)
        self.assertIn(f'name="tax_amount" value="{self.test_tax_amount}"', form)
        self.assertIn(f'name="product_code" value="{self.test_product_code}"', form)
        self.assertIn(f'name="transaction_uuid" value="{self.test_uuid}"', form)
        self.assertIn(f'name="success_url" value="{self.test_success_url}"', form)
        self.assertIn(f'name="failure_url" value="{self.test_failure_url}"', form)
        self.assertIn('name="signed_field_names"', form)
        self.assertIn('name="signature"', form)

    @patch('requests.get')
    def test_get_status_success(self, mock_get):
        """Test successful status check."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "COMPLETE"}
        mock_get.return_value = mock_response

        payment = EsewaPayment(
            product_code=self.test_product_code,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        status = payment.get_status(dev=True)
        
        self.assertEqual(status, "COMPLETE")
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_status_failure(self, mock_get):
        """Test failed status check."""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Error message"
        mock_get.return_value = mock_response

        payment = EsewaPayment(
            product_code=self.test_product_code,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        
        with self.assertRaises(requests.exceptions.RequestException):
            payment.get_status(dev=True)

    def test_is_completed(self):
        """Test transaction completion check."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        
        # Mock get_status to return COMPLETE
        with patch.object(payment, 'get_status', return_value="COMPLETE"):
            self.assertTrue(payment.is_completed(dev=True))
        
        # Mock get_status to return other status
        with patch.object(payment, 'get_status', return_value="PENDING"):
            self.assertFalse(payment.is_completed(dev=True))

    def test_verify_signature_valid(self):
        """Test signature verification with valid signature."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        payment.create_signature()
        
        # Create a valid response
        response_data = {
            "transaction_code": "LD5CEH",
            "status": "COMPLETE",
            "total_amount": str(self.test_total_amount),
            "transaction_uuid": self.test_uuid,
            "product_code": self.test_product_code,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": payment.signature
        }
        response_json = json.dumps(response_data)
        response_base64 = base64.b64encode(response_json.encode()).decode()
        
        is_valid, data = payment.verify_signature(response_base64)
        self.assertTrue(is_valid)
        self.assertIsNotNone(data)
        self.assertEqual(data["status"], "COMPLETE")

    def test_verify_signature_invalid(self):
        """Test signature verification with invalid signature."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        payment.create_signature()
        
        # Create an invalid response with wrong signature
        response_data = {
            "transaction_code": "LD5CEH",
            "status": "COMPLETE",
            "total_amount": str(self.test_total_amount),
            "transaction_uuid": self.test_uuid,
            "product_code": self.test_product_code,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": "invalid_signature"
        }
        response_json = json.dumps(response_data)
        response_base64 = base64.b64encode(response_json.encode()).decode()
        
        is_valid, data = payment.verify_signature(response_base64)
        self.assertFalse(is_valid)
        self.assertIsNone(data)

    def test_log_transaction(self):
        """Test transaction logging."""
        payment = EsewaPayment(
            product_code=self.test_product_code,
            amount=self.test_amount,
            total_amount=self.test_total_amount,
            transaction_uuid=self.test_uuid
        )
        payment.create_signature()
        
        with patch('logging.getLogger') as mock_logger:
            mock_log = MagicMock()
            mock_logger.return_value = mock_log
            payment.log_transaction()
            
            mock_log.info.assert_called_once()
            log_data = mock_log.info.call_args[0][0]
            self.assertEqual(log_data["Transaction UUID"], self.test_uuid)
            self.assertEqual(log_data["Product Code"], self.test_product_code)
            self.assertEqual(log_data["Total Amount"], self.test_amount)
            self.assertEqual(log_data["Signature"], payment.signature)

    def test_equality_comparison(self):
        """Test equality comparison between EsewaPayment instances."""
        payment1 = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key
        )
        payment2 = EsewaPayment(
            product_code=self.test_product_code,
            secret_key=self.test_secret_key
        )
        payment3 = EsewaPayment(
            product_code="DIFFERENT",
            secret_key=self.test_secret_key
        )
        
        self.assertEqual(payment1, payment2)
        self.assertNotEqual(payment1, payment3)
        self.assertNotEqual(payment1, "not a payment object")

if __name__ == '__main__':
    unittest.main() 