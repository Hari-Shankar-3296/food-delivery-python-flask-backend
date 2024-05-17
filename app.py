# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import Config
from models import db, User, Restaurant, Dish, DeliveryPartner
from services import create_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)


@app.route('/register/user', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    address = data.get('address')
    mobile = data.get('mobile')
    user_type = data.get('user_type')

    if not name or not username or not password:
        return jsonify({'error': 'Name, username, and password are required.'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'msg': '', 'error': 'Username is already taken'}), 400

    try:
        create_user(name, username, password, address, mobile, user_type)
        return jsonify({'msg': 'User created successfully.', 'error': ''}), 201
    except Exception as e:
        return jsonify({'msg': 'Error in creating user', 'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    if user_type == "RESTAURANT":
        user = Restaurant.query.filter_by(username=username).first()
    elif user_type == "DELIVERY_PARTNER":
        user = DeliveryPartner.query.filter_by(username=username).first()
    else:
        user = User.query.filter_by(username=username).first()

    if not user or not user.password:
        return jsonify({'error': 'Invalid username or password.'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({'user_token': access_token}), 200


@app.route('/register/restaurant', methods=['POST'])
@jwt_required()
def register_restaurant():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    mobile = data.get('mobile')
    address = data.get('address')
    image_url = data.get('image_url')
    cuisine = data.get('cuisine')
    open_time = data.get('open_time')
    close_time = data.get('close_time')

    # Check if all required fields are present
    if not username or not password or not name or not mobile or not address or not cuisine or not open_time or not close_time:
        return jsonify({'msg': '', 'error': 'All fields are required'}), 400

    # Check if the username is already taken
    existing_restaurant = Restaurant.query.filter_by(username=username).first()
    if existing_restaurant:
        return jsonify({'msg': '', 'error': 'Username is already taken'}), 400

    # Create a new restaurant instance
    new_restaurant = Restaurant(
        username=username,
        password=password,
        name=name,
        mobile=mobile,
        address=address,
        image_url=image_url,
        cuisine=cuisine,
        open_time=open_time,
        close_time=close_time
    )

    # Add the restaurant to the database
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({'msg': 'Restaurant registered successfully', 'error': ''}), 201


@app.route('/register/delivery-partner', methods=['POST'])
def register_delivery_partner():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    mobile = data.get('mobile')

    # Check if all required fields are present
    if not username or not password or not name or not mobile:
        return jsonify({'msg': '', 'error': 'All fields are required'}), 400

    # Check if the username is already taken
    existing_delivery_partner = DeliveryPartner.query.filter_by(username=username).first()
    if existing_delivery_partner:
        return jsonify({'msg': '', 'error': 'Username is already taken'}), 400

    # Create a new delivery partner instance
    new_delivery_partner = DeliveryPartner(
        username=username,
        password=password,
        name=name,
        mobile=mobile
    )

    # Add the delivery partner to the database
    db.session.add(new_delivery_partner)
    db.session.commit()

    return jsonify({'msg': 'Delivery partner registered successfully', 'error': ''}), 201


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
                        "rating": restaurant.rating,
                        "offers": restaurant.offers}
                       for restaurant in restaurants]

    return jsonify({'restaurants': restaurant_list}), 200


@app.route('/dishes/<int:restaurant_id>', methods=['POST'])
@jwt_required()
def create_dish(restaurant_id):
    current_user_id = get_jwt_identity()
    # Validate if the restaurant belongs to the current user
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if not restaurant:
        return jsonify({'msg': 'Restaurant not found'}), 404

    data = request.json
    dish_data = data.get('dish')
    if not dish_data:
        return jsonify({'msg': 'Dish data missing'}), 400

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

    return jsonify({'msg': 'Dish added successfully'}), 201


@app.route('/dishes/<int:restaurant_id>', methods=['GET'])
@jwt_required()
def get_dishes(restaurant_id):
    current_user_id = get_jwt_identity()

    # Fetch dishes for the provided restaurant_id
    dishes = Dish.query.filter_by(restaurant_id=restaurant_id).all()

    # Construct response data
    dish_list = [{
        'id': dish.id,
        'name': dish.name,
        'description': dish.description,
        'image_url': dish.image_url,
        'price': dish.price,
        'rating': dish.rating,
        'restaurant_id': dish.restaurant_id
    } for dish in dishes]

    return jsonify({'dishes': dish_list}), 200


if __name__ == '__main__':
    app.run(debug=True)
