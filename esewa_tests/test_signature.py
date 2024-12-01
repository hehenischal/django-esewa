import unittest
from esewa.signature import generate_signature

class TestEsewaSignature(unittest.TestCase):
    def test_generate_signature_valid(self):
        key = "testkey"
        total_amount = "1000"
        transaction_uuid = "1234abcd"
        product_code = "EPAYTEST"

        signature = generate_signature(total_amount, transaction_uuid, key, product_code)
        self.assertIsInstance(signature, str)
        self.assertTrue(len(signature) > 0)

    def test_generate_signature_missing_params(self):
        with self.assertRaises(ValueError):
            generate_signature("", "1234abcd")
        with self.assertRaises(ValueError):
            generate_signature("1000", "")

if __name__ == "__main__":
    unittest.main()
