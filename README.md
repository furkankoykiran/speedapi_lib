# speedapi_lib

This is a Python library for interacting with the Speed API and managing Lightning Network invoices.

## Installation

You can install this library from your private GitHub repository:

```bash
pip install speedapi-lib
```

## Usage

```python
from speedapi_lib.speedapi import SpeedAPI

# Initialize the SpeedAPI class with user-provided inputs
api = SpeedAPI(secret_key='your_secret_key', base_url='https://api.tryspeed.com')

# Get balance in SATS
balance = api.get_balance_sats()
print(f"Balance: {balance} SATS")

# Decode and print invoice details
invoice_str = "your_invoice_here"
invoice_info = api.get_invoice_info(invoice_str)
print(invoice_info)

# Pay the invoice if balance is sufficient
if balance >= invoice_info["amount"]:
    payment_response = api.pay_invoice(invoice_str)
    print("Payment successful:", payment_response)
else:
    print("Insufficient balance to pay invoice")

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.