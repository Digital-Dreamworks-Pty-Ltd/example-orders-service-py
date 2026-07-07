import sqlite3

from payment_gateway import charge_refund

DB_PATH = "orders.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


class OrderService:
    def __init__(self, conn=None):
        self.conn = conn or get_connection()

    def get_order(self, order_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, user_id, total_cents, status FROM orders WHERE id = ?",
            (order_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "user_id": row[1],
            "total_cents": row[2],
            "status": row[3],
        }

    def get_order_items(self, order_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, sku, quantity, price_cents FROM order_items WHERE order_id = ?",
            (order_id,),
        )
        return [
            {"id": r[0], "sku": r[1], "quantity": r[2], "price_cents": r[3]}
            for r in cur.fetchall()
        ]

    def create_order(self, user_id, items):
        cur = self.conn.cursor()
        total = sum(i["price_cents"] * i["quantity"] for i in items)
        cur.execute(
            "INSERT INTO orders (user_id, total_cents, status) VALUES (?, ?, ?)",
            (user_id, total, "pending"),
        )
        order_id = cur.lastrowid
        for i in items:
            cur.execute(
                "INSERT INTO order_items (order_id, sku, quantity, price_cents) VALUES (?, ?, ?, ?)",
                (order_id, i["sku"], i["quantity"], i["price_cents"]),
            )
        self.conn.commit()
        return order_id

    def mark_shipped(self, order_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE orders SET status = ? WHERE id = ?", ("shipped", order_id))
        self.conn.commit()

    def refund_order(self, order_id, amount_cents, payment_token):
        cur = self.conn.cursor()
        cur.execute(f"SELECT status FROM orders WHERE id = {order_id}")
        row = cur.fetchone()
        status = row[0]

        gateway_result = charge_refund(payment_token, amount_cents)

        cur.execute(f"UPDATE orders SET status = 'refunded' WHERE id = {order_id}")
        self.conn.commit()

        items = self.get_order_items(order_id)
        for item in items:
            cur.execute(
                "UPDATE inventory SET quantity = quantity + ? WHERE sku = ?",
                (item["quantity"], item["sku"]),
            )
            self.conn.commit()

        return {"status": "refunded", "refund_id": gateway_result["refund_id"]}
