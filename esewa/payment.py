import base64
import requests
from django.conf import settings
import logging
import requests
import json
from typing import Dict, Optional, Tuple
from .signature import generate_signature

class EsewaPayment:
    '''
    A class to handle eSewa payment integration.
    Attributes:
    secret_key (str): Secret Key for HMAC signature generation.
    product_code (str): Your Product Code.
    Methods:
    generate_signature(params):
    create_payment_form(amount, tax_amount, total_amount, transaction_uuid, success_url, failure_url):
    send_payment_request(amount, tax_amount, total_amount, transaction_uuid, success_url, failure_url):
    check_transaction_status(product_code, total_amount, transaction_uuid):
    
    '''
    def __init__(self, product_code="EPAYTEST", success_url=None, failure_url=None, secret_key=None):
        """
        Initializes the EsewaPayment instance.

        :param product_code: The product code provided by eSewa.
        :param success_url: Optional. URL to redirect upon successful payment.
        :param failure_url: Optional. URL to redirect upon payment failure.
        :param secret_key: Optional. Secret key for the eSewa API.
        """
        # Handle secret key
        if secret_key:
            self.secret_key = secret_key
            print("Secret key is provided")
        else:
            logger = logging.getLogger(__name__)
            if not hasattr(settings, 'ESEWA_SECRET_KEY'):
                logger.warning(
                    "Using default secret key for EsewaPayment. "
                    "Please set ESEWA_SECRET_KEY in settings."
                )
            self.secret_key = secret_key or getattr(settings, 'ESEWA_SECRET_KEY', "8gBm/:&EnhH.1/q")
        
        # Handle success URL
        if success_url:
            self.success_url = success_url
            print("Success URL is provided")
        else:
            logger = logging.getLogger(__name__)
            if not hasattr(settings, 'ESEWA_SUCCESS_URL'):
                logger.warning(
                    "Using default success URL for EsewaPayment. "
                    "Please set ESEWA_SUCCESS_URL in settings."
                )
            self.success_url = success_url or getattr(settings, 'ESEWA_SUCCESS_URL', "http://localhost:8000/success/")
        
        # Handle failure URL
        if failure_url:
            self.failure_url = failure_url
            print("Failure URL is provided")
        else:
            logger = logging.getLogger(__name__)
            if not hasattr(settings, 'ESEWA_FAILURE_URL'):
                logger.warning(
                    "Using default failure URL for EsewaPayment. "
                    "Please set ESEWA_FAILURE_URL in settings."
                )
            self.failure_url = failure_url or getattr(settings, 'ESEWA_FAILURE_URL', "http://localhost:8000/failure/")
        self.product_code = product_code


    
    def create_signature(
            self, 
            total_amount: float, 
            transaction_uuid: str
            ) -> str:
        """
        Generates HMAC-SHA256 signature for eSewa payment gateway.
        :param total_amount: The total amount to be paid.
        :param transaction_uuid: A unique identifier for the transaction.
        :return: The generated signature.
        """
        self.amount = total_amount
        self.uuid = transaction_uuid
        self.signature = generate_signature(total_amount, transaction_uuid, self.secret_key, self.product_code)
        return self.signature

    
    def generate_redirect_url():
        pass

    def refund_payment():
        pass

    def simulate_payment():
        pass

    def generate_form(self)->Dict[str, str]:
        """
        generate HTML code for eSewa payment gateway
        """
        payload = {
            "amount": self.amount,
            "product_delivery_charge": "0",
            "product_service_charge": "0",
            "total_amount": self.amount,
            "tax_amount": 0,
            "product_code": self.product_code,
            "transaction_uuid": self.uuid,
            "success_url": self.success_url,
            "failure_url": self.failure_url,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": self.signature
        }

        form= ""
        for key, value in payload.items():
            form += f'<input type="hidden" name="{key}" value="{value}">'

        return form


    def get_status(self, dev: bool) -> str:
        """
        Retrieves the transaction status from eSewa based on the environment.
        :param dev: If True, use the testing environment URL. If False, use the production environment URL.
        :return: The status of the transaction as returned by the eSewa API.
        """
        status_url_testing = f"https://uat.esewa.com.np/api/epay/transaction/status/?product_code={self.product_code}&total_amount={self.amount}&transaction_uuid={self.uuid}"
        status_url_prod = f"https://epay.esewa.com.np/api/epay/transaction/status/?product_code={self.product_code}&total_amount={self.amount}&transaction_uuid={self.uuid}"

        url = status_url_testing if dev else status_url_prod
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Error fetching status: {response.text}")

        response_data = response.json()
        return response_data.get("status", "UNKNOWN")


    def is_completed(self, dev: bool) -> bool:
        """
        Checks if the transaction is completed.
        :param dev: Use the testing environment if True, production otherwise.
        :return: True if the transaction is completed, False otherwise.
        """
        return self.get_status(dev) == "COMPLETE"

    def __eq__(self, value: object) -> bool:
        """
        Compare this EsewaPayment instance with another instance for equality.

        Args:
            value (object): The object to compare with.

        Returns:
            bool: True if the given object is an instance of EsewaPayment and has the same
                secret_key and product_code as this instance, False otherwise.
        """
        ''''''
        if not isinstance(value, EsewaPayment):
            return False
        return self.secret_key == value.secret_key and self.product_code == value.product_code
        
    def verify_signature(
            self,
        response_body_base64: str,
    ) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Verifies the signature of an eSewa response.
        
        Args:
            response_body_base64 (str): The Base64-encoded response body.
        
        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: 
                A tuple where the first element is a boolean indicating the validity of the signature,
                and the second element is a dictionary of the decoded response data if the signature is valid, otherwise None.
        """
        try:
            response_body_json = base64.b64decode(response_body_base64).decode("utf-8")
            response_data: Dict[str, str] = json.loads(response_body_json)
            
            signed_field_names: str = response_data["signed_field_names"]
            received_signature: str = response_data["signature"]
            
            field_names = signed_field_names.split(",")
            message: str = ",".join(
                f"{field_name}={response_data[field_name]}" for field_name in field_names
            )
            is_valid: bool = received_signature == self.signature
            return is_valid, response_data if is_valid else None
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False, None


    def log_transaction(self):
        """
        Logs the transaction details for debugging and record-keeping.
        """
        logger = logging.getLogger(__name__)
        logger.info({
            "Transaction UUID": self.uuid,
            "Product Code": self.product_code,
            "Total Amount": self.amount,
            "Signature": self.signature
        })


if __name__ == "__main__":
    payment = EsewaPayment()
    signature = payment.create_signature(100, "11-201-13")
    print(f"Generated Signature: {signature}")
    payload = payment.generate_form()
    print(f"Generated Payload: {payload}")
    status = payment.get_status(dev=True)
    print(f"Transaction Status: {status}")
    completed = payment.is_completed(dev=True)
    print(f"Transaction Completed: {completed}")
    verified, response_data = payment.verify_signature("eyJ0cmFuc2FjdGlvbl9jb2RlIjoiMExENUNFSCIsInN0YXR1cyI6IkNPTVBMRVRFIiwidG90YWxfYW1vdW50IjoiMSwwMDAuMCIsInRyYW5zYWN0aW9uX3V1aWQiOiIyNDA2MTMtMTM0MjMxIiwicHJvZHVjdF9jb2RlIjoiTlAtRVMtQUJISVNIRUstRVBBWSIsInNpZ25lZF9maWVsZF9uYW1lcyI6InRyYW5zYWN0aW9uX2NvZGUsc3RhdHVzLHRvdGFsX2Ftb3VudCx0cmFuc2FjdGlvbl91dWlkLHByb2R1Y3RfY29kZSxzaWduZWRfZmllbGRfbmFtZXMiLCJzaWduYXR1cmUiOiJNcHd5MFRGbEhxcEpqRlVER2ljKzIybWRvZW5JVFQrQ2N6MUxDNjFxTUFjPSJ9 ")


