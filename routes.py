from flask import Flask, request, jsonify

from order_service import OrderService

app = Flask(__name__)


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    service = OrderService()
    order_id = service.create_order(data["user_id"], data["items"])
    return jsonify({"order_id": order_id}), 201


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    service = OrderService()
    order = service.get_order(order_id)
    if not order:
        return jsonify({"error": "not found"}), 404
    order["items"] = service.get_order_items(order_id)
    return jsonify(order)


@app.route("/orders/<int:order_id>/ship", methods=["POST"])
def ship_order(order_id):
    service = OrderService()
    service.mark_shipped(order_id)
    return jsonify({"status": "shipped"})
