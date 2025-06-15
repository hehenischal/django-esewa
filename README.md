# Django-esewa

A simple, developer-friendly package for integrating the eSewa Payment Gateway into Django applications.

# Learn Django (100% Free) at your own pace
- [django-tutorial.dev Payment integration](https://django-tutorial.dev/course/payment-integration/esewa-integration/django-esewa-package/)

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


Even though you can use the `generate_signature`(from django_esewa) function without creating an object of `EsewaPayment`, if you want to use other features, you need to instantiate an object of the class `EsewaPayment`. 


---
## Usage
 All the amounts like amount, tax_amount, total_amount, product_delivery_charge, product_service_charge will be defaulted to 0. 
 success_url will defaulted to `http://localhost:8000/success/` and failure_url will be defaulted to `http://localhost:8000/failure/`. Secret key will be defaulted to `"8gBm/:&EnhH.1/q"`. Product code will be defaulted to `EPAYTEST`. Transaction uuid will be defaulted to `None`.

### Generating HTML Form
 > Views.py
```python 
from django_esewa import EsewaPayment

def confirm_order(request,id):
    order = Order.objects.get(id=id)

    payment = EsewaPayment(
        product_code=order.code,
        success_url="http://yourdomain.com/success/",
        failure_url="http://yourdomain.com/failure/",
        amount=order.amount,
        tax_amount=calculate_tax(),
        total_amount=order.total_amount,
        product_delivery_charge=order.delivery_charge,
        product_service_charge=order.service_charge
        transaction_uuid="transaction uuid",
        secret_key="your_secret_key",

    )
    signature = payment.create_signature() #Saves the signature as well as return it

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
from django_esewa import generate_signature

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
from django_esewa import EsewaPayment

payment = EsewaPayment(
    product_code="EPAYTEST",
        success_url="http://localhost:8000/success/",
        failure_url="http://localhost:8000/failure/",
        amount=100,
        tax_amount=0,
        total_amount=100,
        product_service_charge=0,
        product_delivery_charge=0,
        transaction_uuid="11-200-111sss1",
)
```

**Signature generation**

```python
signature = payment.create_signature()
```

**Form Generation**

```python
form = payment.generate_form()
```

### Settings

From Version 1.0.8, We are improvising this package to work not only with Django but also with Other Python Frameworks. so there is no Explicit configuration for Django Settings. Feel free to use Previous configuration and then dynamically use the credentials using settings.getattr or python-decouple

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
