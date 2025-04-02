    # flask_app.py
from flask import Flask, jsonify, request
import os   

# Create a Flask application instance
app = Flask(__name__)

# Simple in-memory database
users_db = {}
data_store = []

# Basic route that returns a JSON response
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to my Flask API!",
        "status": "success"
    })

# Route that accepts GET requests with query parameters
@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    return jsonify({
        "message": f"Hello, {name}!",
        "status": "success"
    })

# Route that accepts POST requests with JSON data
@app.route('/api/data', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    # Store the data in our data store
    data_store.append(data)
    return jsonify({
        "message": "Data received and stored successfully",
        "received_data": data,
        "total_records": len(data_store),
        "status": "success"
    })

# Route to get all stored data
@app.route('/api/data', methods=['GET'])
def get_all_data():
    return jsonify({
        "message": "Retrieved all stored data",
        "data": data_store,
        "total_records": len(data_store),
        "status": "success"
    })

# Route that demonstrates path parameters and user storage
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if user:
        return jsonify({
            "message": f"Found user with ID: {user_id}",
            "user": user,
            "status": "success"
        })
    return jsonify({
        "message": f"User with ID {user_id} not found",
        "status": "error"
    }), 404

# Route to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'id' not in data or 'name' not in data:
        return jsonify({
            "message": "Invalid user data. Required fields: id, name",
            "status": "error"
        }), 400
    
    user_id = data['id']
    if user_id in users_db:
        return jsonify({
            "message": f"User with ID {user_id} already exists",
            "status": "error"
        }), 409
    
    users_db[user_id] = data
    return jsonify({
        "message": "User created successfully",
        "user": data,
        "status": "success"
    }), 201

# Route to get all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    return jsonify({
        "message": "Retrieved all users",
        "users": list(users_db.values()),
        "total_users": len(users_db),
        "status": "success"
    })

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)         
    