from flask import Flask, jsonify, request
from models import db, User, Farmer, Crop, Order, MarketPrice
import logging

logging.basicConfig(level=logging.INFO)

def create_routes(app):

    @app.before_request
    def log_request_info():
        app.logger.info('Headers: %s', request.headers)
        app.logger.info('Body: %s', request.get_data())

    @app.route('/')
    def home():
        return "Backend & Database Ready!"

    # User APIs
    @app.route('/users', methods=['POST'])
    def add_user():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        app.logger.info(f"Received data for new user: {data}")
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    # Farmer APIs
    @app.route('/farmers', methods=['POST'])
    def add_farmer():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        app.logger.info(f"Received data for new farmer: {data}")
        required_fields = ['name', 'phone', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        new_farmer = Farmer(name=data['name'], phone=data['phone'], location=data['location'])
        db.session.add(new_farmer)
        db.session.commit()
        return jsonify(new_farmer.to_dict()), 201

    @app.route('/farmers', methods=['GET'])
    def get_farmers():
        farmers = Farmer.query.all()
        return jsonify([farmer.to_dict() for farmer in farmers])

    # Crop APIs
    @app.route('/crops', methods=['POST'])
    def add_crop():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        app.logger.info(f"Received data for new crop: {data}")
        required_fields = ['name', 'farmer_id', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        new_crop = Crop(
            farmer_id=data['farmer_id'],
            name=data['name'],
            type=data.get('type', ''),
            quantity=data['quantity']
        )
        db.session.add(new_crop)
        db.session.commit()
        return jsonify(new_crop.to_dict()), 201

    @app.route('/crops', methods=['GET'])
    def get_crops():
        crops = Crop.query.all()
        return jsonify([crop.to_dict() for crop in crops])

    # Order APIs
    @app.route('/orders', methods=['POST'])
    def add_order():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        app.logger.info(f"Received data for new order: {data}")
        required_fields = ['crop_id', 'buyer_name', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        new_order = Order(
            crop_id=data['crop_id'],
            buyer_name=data['buyer_name'],
            quantity=data['quantity'],
            status=data.get('status', 'Pending')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), 201

    @app.route('/orders', methods=['GET'])
    def get_orders():
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])

    @app.route('/orders/<int:order_id>', methods=['PUT'])
    def update_order(order_id):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        order.status = data.get('status', order.status)
        db.session.commit()
        return jsonify(order.to_dict())

    # Market Price APIs
    @app.route('/market_prices', methods=['POST'])
    def add_price():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        app.logger.info(f"Received data for new market price: {data}")
        required_fields = ['crop_name', 'price_per_kg']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        new_price = MarketPrice(
            crop_name=data['crop_name'],
            price_per_kg=data['price_per_kg']
        )
        db.session.add(new_price)
        db.session.commit()
        return jsonify(new_price.to_dict()), 201

    @app.route('/market_prices', methods=['GET'])
    def get_prices():
        prices = MarketPrice.query.all()
        return jsonify([price.to_dict() for price in prices])
