# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import Config
from models import db, User, Restaurant
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

    if not name or not username or not password:
        return jsonify({'error': 'Name, username, and password are required.'}), 400

    try:
        create_user(name, username, password)
        return jsonify({'message': 'User created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    return jsonify({'access_token': access_token}), 200


@app.route('/restaurants', methods=['GET'])
@jwt_required()
def get_restaurants():
    current_user_id = get_jwt_identity()
    # You can use current_user_id to fetch user details if needed

    # Get all restaurant lists
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': restaurant.id, 'name': restaurant.name} for restaurant in restaurants]

    return jsonify(restaurant_list), 200


if __name__ == '__main__':
    app.run(debug=True)
