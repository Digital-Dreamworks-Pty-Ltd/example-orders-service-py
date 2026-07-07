import sqlite3

import pytest

from order_service import OrderService
from payment_gateway import PaymentGatewayError, charge_refund


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.executescript(open("schema.sql").read())
    return conn


def test_create_order_computes_total_and_persists_items():
    service = OrderService(make_conn())
    order_id = service.create_order(
        user_id=1,
        items=[
            {"sku": "WIDGET", "quantity": 2, "price_cents": 500},
            {"sku": "GADGET", "quantity": 1, "price_cents": 1000},
        ],
    )

    order = service.get_order(order_id)
    assert order["total_cents"] == 2000
    assert order["status"] == "pending"

    items = service.get_order_items(order_id)
    assert len(items) == 2


def test_get_order_returns_none_when_missing():
    service = OrderService(make_conn())
    assert service.get_order(999) is None


def test_mark_shipped_updates_status():
    service = OrderService(make_conn())
    order_id = service.create_order(
        user_id=1, items=[{"sku": "WIDGET", "quantity": 1, "price_cents": 500}]
    )

    service.mark_shipped(order_id)

    assert service.get_order(order_id)["status"] == "shipped"

