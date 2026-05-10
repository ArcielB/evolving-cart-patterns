from dataclasses import dataclass
from decimal import Decimal

from .money import money


@dataclass(frozen=True)
class PaymentReceipt:
    status: str
    reference: str


class ExternalPaymentProvider:
    def submit_payment(self, payload: dict[str, str]) -> dict[str, str]:
        channel = payload["channel"]
        if channel not in {"credit_card", "paypal", "bank_transfer"}:
            return {"state": "declined", "provider_id": "unsupported-channel"}

        state = "pending" if channel == "bank_transfer" else "approved"
        provider_id = f"provider-{channel}-{payload['customer']}-{payload['amount']}"
        return {"state": state, "provider_id": provider_id}


class PaymentAdapter:
    def __init__(self, provider: ExternalPaymentProvider | None = None) -> None:
        self.provider = provider or ExternalPaymentProvider()

    def pay(
        self, amount: Decimal | int | str, payment_method: str, customer_email: str
    ) -> PaymentReceipt:
        payload = {
            "amount": str(money(amount)),
            "channel": payment_method,
            "customer": customer_email,
        }
        response = self.provider.submit_payment(payload)

        if response["state"] == "declined":
            raise ValueError(f"Unknown payment method: {payment_method}")

        return PaymentReceipt(
            status=response["state"],
            reference=response["provider_id"],
        )
