# speedapi_lib

This is a Python library for interacting with the Speed API and managing Lightning Network invoices.

## Installation

You can install this library from your private GitHub repository:

```bash
pip install speedapi-lib
```

## Usage

```python
from speedapi_lib.api_client import SpeedAPIClient
from speedapi_lib.invoice import Invoice
from speedapi_lib.config import AppConfig

config = AppConfig()

client = SpeedAPIClient(secret_key=config.SECRET_KEY, base_url=config.BASE_URL)
balance = client.get_balance_sats()
print(f"Balance: {balance} SATS")

invoice_str = "your_invoice_here"
invoice = Invoice(invoice_str)
invoice_info = invoice.get_info()
print(invoice_info)

if balance >= invoice_info["amount"]:
    payment = client.pay_invoice(invoice_str)
    print(payment)
else:
    print("Insufficient balance to pay invoice")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.