# app.py
from flask import Flask, request, jsonify
from config import Config
from models import db, User
from services import create_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


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


if __name__ == '__main__':
    app.run(debug=True)
