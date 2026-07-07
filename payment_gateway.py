import random


class PaymentGatewayError(Exception):
    pass


def charge_refund(payment_token, amount_cents):
    """Simulates calling out to a third-party payment processor.

    In production this hits a real network service, so it can fail
    independently of anything happening in our own database.
    """
    if random.random() < 0.05:
        raise PaymentGatewayError("Gateway timeout")
    return {
        "refund_id": f"rf_{random.randint(100000, 999999)}",
        "amount_cents": amount_cents,
    }
