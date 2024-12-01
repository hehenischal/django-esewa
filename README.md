# django-esewa
package for easy Esewa Integration 

- This package was created by Nischal Lamichhane as a Last Ditch error to help Python/Django Developers to Integrate E-sewa Payment Gateway into their application. 
- This version is only going to help devs generate necessary HMAC Key for the Signature field. 
- Newer versions will help in status checking for a transaction. (if this package takes off)

## Function signature
```python
def generate_signature(total_amount: float, transaction_uuid: str, key: str = "8gBm/:&EnhH.1/q", product_code: str = "EPAYTEST") -> str:
```

## Usage 
```python
import esewa

signature = esewa.generate_signature()
``` 

### During Developemnt
```python
signature = generate_signature(1000,"123abc")
```

### In Production
```python
signature = generate_signature(1000,"123abc",<your_private_key>,<product_key>)
```
