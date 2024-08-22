import bolt11

class Invoice:
    def __init__(self, invoice: str):
        self.invoice = invoice
        self.decoded_invoice = self._decode_invoice()
    
    def _decode_invoice(self):
        return bolt11.decode(self.invoice)

    def get_info(self) -> dict:
        return {
            "amount": self.decoded_invoice.amount_msat / 1000,
            "timestamp": self.decoded_invoice.date,
            "description": self.decoded_invoice.description,
            "payment_hash": self.decoded_invoice.payment_hash,
            "expiry": self.decoded_invoice.expiry
        }
