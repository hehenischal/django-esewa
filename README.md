# Django-esewa

A simple, developer-friendly package for integrating the eSewa Payment Gateway into Django applications.

## Overview

`django-esewa` was developed by Nischal Lamichhane to simplify eSewa integration for Python/Django developers. It aims to handle common payment gateway tasks like generating HMAC signatures, verifying transactions, and status checks (in future versions).

## Features

- **HMAC Key Generation**: Easily generate the signature required for eSewa requests.
- **Customization**: Configure secret keys, product codes, success URLs, and failure URLs.

### Future Goals

- Transaction status verification.
- Improved documentation for all class methods.

## QuickStart

```bash
pip install django-esewa
```

Note: Ensure you have added necessary settings like `ESEWA_SECRET_KEY`, `ESEWA_SUCCESS_URL`, and `ESEWA_FAILURE_URL` in your `settings.py`.

Even though you can use the `generate_signature` function without creating an object of `EsewaPayment`, if you want to use other features, you need to add `ESEWA_SUCCESS_URL`, `ESEWA_FAILURE_URL` (will fallback to `localhost:8000/success/` & `localhost:8000/failure/`) & `ESEWA_SECRET_KEY` (will fall back to `'8gBm/:&EnhH.1/q'`).

```python
ESEWA_SUCCESS_URL = "localhost:8000/success/"
ESEWA_FAILURE_URL = "localhost:8000/failure/"
ESEWA_SECRET_KEY = "<Custom_key_from_Esewa>"
```
---
## Usage

### Generating HTML Form
 > Views.py
```python 
from esewa import EsewaPayment

def confirm_order(request,id):
    order = Order.objects.get(id=id)
   

    payment = EsewaPayment(
        product_code=order.code,
        success_url="http://yourdomain.com/success/",
        failure_url="http://yourdomain.com/failure/",
        secret_key="your_secret_key"
    )

    context = {
        'form':payment.generate_form()
    }
    return render(request,'order/checkout.html',context)
```
> order/checkout.html
```html
<form action="https://rc-epay.esewa.com.np/api/epay/main/v2/form" method="POST">
    {{form|safe}}
    <button type="submit">Pay with Esewa </button>
</form>
```
---

### Generating a Signature

The `generate_signature` function helps create the HMAC signature required by eSewa for secure transactions.

**Function Signature:**

```python
def generate_signature(
    total_amount: float,
    transaction_uuid: str,
    key: str = "8gBm/:&EnhH.1/q",
    product_code: str = "EPAYTEST"
) -> str:
```

**Example:**

```python
from esewa import generate_signature

# During Development
signature = generate_signature(1000, "123abc")

# In Production
signature = generate_signature(1000, "123abc", "<your_private_key>", "<product_code>")
```
---
### Using the EsewaPayment Class

`EsewaPayment` provides additional configuration options for success and failure URLs.
List of all methods in EsewaPayment:
- `__init__()`
- `create_signature()`
- `generate_form()`
- `get_status()`
- `is_completed()`
- `verify_signature()`
- `log_transaction()`
- `__eq__()`

List of In-development methods:
- `generate_redirect_url()`
- `refund_payment()`
- `simulate_payment()`

---

**Initialization:**

```python
from esewa import EsewaPayment

payment = EsewaPayment(
    product_code="EPAYTEST",
    success_url="http://yourdomain.com/success/",
    failure_url="http://yourdomain.com/failure/",
    secret_key="your_secret_key"
)
```

### Settings

To use custom configurations, add the following keys to your `settings.py`:

```python
# settings.py

ESEWA_SECRET_KEY = "your_secret_key"
ESEWA_SUCCESS_URL = "http://yourdomain.com/success/"
ESEWA_FAILURE_URL = "http://yourdomain.com/failure/"
```

If these settings are missing, the package will use the following defaults:

- `ESEWA_SECRET_KEY`: `"8gBm/:&EnhH.1/q"`
- `ESEWA_SUCCESS_URL`: `"http://localhost:8000/success/"`
- `ESEWA_FAILURE_URL`: `"http://localhost:8000/failure/"`

--- 
## Contributing

### Current To-Do List

- Write documentation for all methods in the `EsewaPayment` class.
- Add refund method

### How to Contribute

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes with clear messages.
4. Submit a pull request (PR) with a detailed description of your changes.

## Credits

`django-esewa` is maintained by Nischal Lamichhane. This package was created as a last-ditch effort to help Python/Django developers integrate eSewa Payment Gateway efficiently.