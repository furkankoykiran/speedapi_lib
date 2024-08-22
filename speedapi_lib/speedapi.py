import requests
import bolt11
import base64

class SpeedAPI:
    def __init__(self, secret_key: str, base_url: str):
        self.secret_key = secret_key
        self.base_url = base_url
        self.base64_key = self._encode_secret_key(secret_key)

    def _encode_secret_key(self, secret_key: str) -> str:
        secret_key_bytes = f"{secret_key}:".encode("ascii")
        return base64.b64encode(secret_key_bytes).decode("ascii")

    def get_balance_sats(self) -> float:
        url = f"{self.base_url}/balances"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.base64_key}",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        balance = next(item["amount"] for item in data["available"] if item["target_currency"] == "SATS")
        return balance

    def pay_invoice(self, invoice: str) -> dict:
        url = f"{self.base_url}/send"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {self.base64_key}",
            "content-type": "application/json"
        }
        payload = {
            "currency": "SATS",
            "withdraw_method": "lightning",
            "withdraw_request": invoice
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def get_invoice_info(self, invoice: str) -> dict:
        decoded_invoice = bolt11.decode(invoice)
        return {
            "amount": decoded_invoice.amount_msat / 1000,
            "timestamp": decoded_invoice.date,
            "description": decoded_invoice.description,
            "payment_hash": decoded_invoice.payment_hash,
            "expiry": decoded_invoice.expiry
        }
