CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_cents INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'  -- pending | shipped | refunded
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE inventory (
    sku TEXT PRIMARY KEY,
    quantity INTEGER NOT NULL
);
