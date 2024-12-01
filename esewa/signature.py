import hmac
import hashlib
import base64

def generate_signature(total_amount: float, transaction_uuid: str, key: str = "8gBm/:&EnhH.1/q", product_code: str = "EPAYTEST") -> str:
    """generates hmac sha256 signature for eSewa payment gateway

    Args:
        total_amount (float): will be processed as a string
        transaction_uuid (str): will be processed as a string
        key (_type_, optional): your private key after buying API. Defaults to "8gBm/:&EnhH.1/q".
        product_code (str, optional): your product code from database. Defaults to "EPAYTEST".

    Raises:
        ValueError: Impropervalues for 'total_amount' and 'transaction_uuid'
        RuntimeError: Failed to generate signature

    Returns:
        str: returns the generated signature
    """
    if not total_amount or not transaction_uuid:
        raise ValueError("Both 'total_amount' and 'transaction_uuid' are required.")

    try:
        message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        key = key.encode('utf-8')
        message = message.encode('utf-8')

        # Generate HMAC-SHA256 digest
        hmac_sha256 = hmac.new(key, message, hashlib.sha256)
        digest = hmac_sha256.digest()

        # Convert to Base64
        signature = base64.b64encode(digest).decode('utf-8')
        return signature
    except Exception as e:
        raise RuntimeError(f"Failed to generate signature: {e}")



if __name__ == "__main__":
    signature = generate_signature(total_amount=1000, transaction_uuid="1234abcd")
    print(f"Generated Signature: {signature}")
