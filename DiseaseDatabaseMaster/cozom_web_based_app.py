from flask import Flask, jsonify, render_template
import sys
import os

# Adding the project directory to the Python path to resolve module not found error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cozom.reader import readDatabase
from cozom.models import Symptom, Condition, BodyPart  # Importing relevant classes

app = Flask(__name__)

data = None

# Route to display the home page
@app.route('/')
def home():
    return "Welcome to the Cozom Health Assessment Web Application"

# Route to display the database information (example route)
@app.route('/database')
def get_database():
    if data:
        # Custom serialize all parts in the data
        serialized_data = [serialize(part) for part in data]
        return jsonify(serialized_data)
    else:
        return "No data available", 404

# Route for Symptom Checker
@app.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html')

# Route for Body Map
@app.route('/body-map')
def body_map():
    return render_template('body_map.html')

# Helper function to serialize custom objects
def serialize(obj):
    if isinstance(obj, BodyPart):
        return {
            "id": obj.id,
            "name": obj.name,
            "symptoms": [serialize(symptom) for symptom in obj.symptoms()]
        }
    elif isinstance(obj, Symptom):
        return {
            "id": obj.id,
            "name": obj.name,
            "conditions": [serialize(condition) for condition in obj.conditions()]
        }
    elif isinstance(obj, Condition):
        return {
            "id": obj.id,
            "name": obj.name,
            "about": obj.about
        }
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        return str(obj)

if __name__ == "__main__":
    # Loading the database at startup
    data = readDatabase(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
    app.run(debug=True, host='0.0.0.0', port=5001)
