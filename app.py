from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
from dotenv import load_dotenv
import os
import requests


app = Flask(__name__)
CORS(app)
# MongoDB Connection
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["trip_management"]
trips_collection = db["trips"]
customers_collection = db["customers"]

# dapr routes ( micro-controller implemenentation )
@app.route('/save_trip', methods=['POST'])
def save_trip():
    trip_data = request.json
    state_data = [{"key": trip_data["id"], "value": trip_data}]
    dapr_url = "http://localhost:3500/v1.0/state/statestore"
    response = requests.post(dapr_url, json=state_data)
    return jsonify(response.json())

@app.route('/get_trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    dapr_url = f"http://localhost:3500/v1.0/state/statestore/{trip_id}"
    response = requests.get(dapr_url)
    return jsonify(response.json())
@app.route('/')
def index():
    return render_template('index.html')

# getting the API s from the databse for getting the customer details 
@app.route('/get_trips', methods=['GET'])
def get_trips():
    trips = list(trips_collection.find())
    for trip in trips:
        trip['_id'] = str(trip['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(trips)

@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = list(customers_collection.find())
    for customer in customers:
        customer['_id'] = str(customer['_id'])  # Convert ObjectId to string
    return jsonify(customers)

@app.route('/submit', methods=['POST'])
def submit_trip():
    trip_data = request.form.to_dict()
    trips_collection.insert_one(trip_data)
    return jsonify({"message": "Trip submitted successfully!"})

@app.route('/add_customer', methods=['POST'])
def add_customer():
    customer_data = request.form.to_dict()
    customers_collection.insert_one(customer_data)
    return jsonify({"message": "Customer added successfully!"})

@app.route('/delete_trip/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    result = trips_collection.delete_one({"_id": ObjectId(trip_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Trip deleted successfully!"})
    else:
        return jsonify({"message": "Trip not found."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
