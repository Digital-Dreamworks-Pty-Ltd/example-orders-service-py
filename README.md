# orders-service

A small internal service for managing orders: creation, lookup, and shipping.

Backed by SQLite for local dev (`schema.sql`), Flask for the API layer.

## Endpoints

- `POST /orders` — create an order
- `GET /orders/<id>` — fetch an order and its items
- `POST /orders/<id>/ship` — mark an order shipped
