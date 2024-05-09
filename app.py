# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import Config
from models import db, User, Restaurant, Dish
from services import create_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    address = data.get('address')
    mobile = data.get('mobile')

    if not name or not username or not password:
        return jsonify({'error': 'Name, username, and password are required.'}), 400

    try:
        create_user(name, username, password, address, mobile)
        return jsonify({'msg': 'User created successfully.', 'error': ''}), 201
    except Exception as e:
        return jsonify({'msg': 'Error in creating user', 'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.password:
        return jsonify({'error': 'Invalid username or password.'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({'data': {'user_token': access_token}}), 200


@app.route('/restaurants', methods=['GET'])
@jwt_required()
def get_restaurants():
    current_user_id = get_jwt_identity()
    # You can use current_user_id to fetch user details if needed

    # Get all restaurant lists
    restaurants = Restaurant.query.all()
    restaurant_list = [{"id": restaurant.id,
                        "name": restaurant.name,
                        "mobile": restaurant.mobile,
                        "address": restaurant.address,
                        "image_url": restaurant.image_url,
                        "reviews": restaurant.reviews,
                        "distance": restaurant.distance,
                        "expected_delivery_time": restaurant.expected_delivery_time,
                        "cuisine": restaurant.cuisine,
                        "open_time": restaurant.open_time,
                        "close_time": restaurant.close_time,
                        "ratings": restaurant.ratings,
                        "offers": restaurant.offers}
                       for restaurant in restaurants]

    return jsonify({'data': {'restaurants': restaurant_list}}), 200


@app.route('/dishes/<int:restaurant_id>', methods=['POST'])
@jwt_required()
def create_dish(restaurant_id):
    current_user_id = get_jwt_identity()
    # Validate if the restaurant belongs to the current user
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if not restaurant:
        return jsonify({'status': 'error', 'data': {'msg': 'Restaurant not found'}}), 404

    data = request.json
    dish_data = data.get('dish')
    if not dish_data:
        return jsonify({'data': {'msg': 'Dish data missing'}}), 400

    dish = Dish(
        restaurant_id=restaurant_id,
        name=dish_data.get('name'),
        description=dish_data.get('description'),
        image_url=dish_data.get('image_url'),
        price=dish_data.get('price'),
        rating=dish_data.get('rating')
    )
    db.session.add(dish)
    db.session.commit()

    return jsonify({'data': {'msg': 'Dish added successfully'}}), 201


if __name__ == '__main__':
    app.run(debug=True)
