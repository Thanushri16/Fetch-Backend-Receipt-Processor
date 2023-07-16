"""Module app for creating a Receipt Processor web service."""

import os
import uuid
import math
from datetime import datetime
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
receipt_data = {}

def calculate_points(data):
    """Function that calculates the points from a JSON represented receipt data."""
    points = 0
    for char in data["retailer"]:
        if char.isalnum():
            points += 1

    digit_list = list(str(data["total"]).split("."))
    if not (len(digit_list) == 1 or int(digit_list[1]) > 0):
        points += 50

    if float(data["total"]) % 0.25 == 0.0:
        points += 25

    number_of_items = len(data["items"])
    points += ((number_of_items // 2) * 5)

    for item in data["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points += math.ceil(float(item["price"]) * 0.2)

    datetime_obj = datetime.strptime(f'{data["purchaseDate"]}\
                                      {data["purchaseTime"]}', "%Y-%m-%d %H:%M")
    if datetime_obj.day % 2 != 0:
        points += 6

    start = datetime.strptime("14:00", "%H:%M")
    end = datetime.strptime("16:00", "%H:%M")
    if datetime_obj.time() > start.time() and datetime_obj.time() < end.time():
        points += 10
    return points


@app.route('/')
def main():
    """Flask app route for main page."""
    response = make_response('Welcome to the main page of the Receipt Processor Application', 200)
    return response


@app.route('/receipts/process', methods = ['POST'])
def process_receipts():
    """Flask app route that posts a JSON formatted receipt"""

    if not request.headers["Content-Type"] == "application/json":
        # Return invalid response if the payload is not in JSON format
        response = make_response(jsonify({"Error": "The receipt is invalid"}), 400)
        response.headers.add('Content-Type', 'application/json')
        return response

    # Generating a unique id for the receipt
    data = request.json
    id = str(uuid.uuid4())
    data["id"] = id
    receipt_data[id] = data

    # Returning the id as a JSON response
    response = make_response(jsonify({"id": id}), 200)
    response.headers.add('Content-Type', 'application/json')
    return response


@app.route('/receipts/<id>/points', methods = ['GET'])
def get_points(id):
    """Flask app route that gets the points associated with a receipt"""

    if id in receipt_data:
        # Calculate points if the id is in the in-memory data storage
        data = receipt_data[id]
        points = calculate_points(data)
        response = make_response(jsonify({"points": points}), 200)

    else:
        # Return receipt not found for that id
        response = make_response(jsonify({"Error": "No receipt found for that id"}), 404)
    response.headers.add('Content-Type', 'application/json')
    return response


@app.route('/receipts', methods = ['GET'])
def get_receipts():
    """Flask app route that retrieves all the receipts stored"""

    if len(receipt_data.keys()) == 0:
        # Return empty if there no receipts exist
        response = make_response(jsonify({"Error": "No receipts found"}), 404)

    else:
        # Return the receipts as a list of JSON objects
        receipt_list = [val for key, val in receipt_data.items()]
        response = make_response(jsonify({"Receipts": receipt_list}), 200)
    response.headers.add('Content-Type', 'application/json')
    return response


@app.route('/receipts/<id>', methods = ['GET'])
def get_receipt(id):
    """Flask app route that retrieves all information of a receipt based on the id"""

    if id in receipt_data:
        # Return receipt if the id is in the in-memory data storage
        data = receipt_data[id]
        response = make_response(jsonify({"Receipt": data}), 200)

    else:
        # Return receipt not found for that id
        response = make_response(jsonify({"Error": "No receipt found for that id"}), 404)
    response.headers.add('Content-Type', 'application/json')
    return response


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
