from Config import AppConfig
from utils.api_client import SpeedAPIClient
from utils.invoice import Invoice

def main():
    config = AppConfig()

    api_client = SpeedAPIClient(secret_key=config.SPEED_SECRET_KEY, base_url=config.SPEED_BASE_URL)
    sats_balance = api_client.get_balance_sats()
    print(f"Balance: {sats_balance} SATS")

    invoice_str = input("Enter invoice: ")
    invoice = Invoice(invoice_str)
    invoice_info = invoice.get_info()
    print(invoice_info)

    if sats_balance >= invoice_info["amount"]:
        payment_response = api_client.pay_invoice(invoice_str)
        print("Payment response:", payment_response)
    else:
        print("Insufficient balance to pay invoice")

if __name__ == "__main__":
    main()
