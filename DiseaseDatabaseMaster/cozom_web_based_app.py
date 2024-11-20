from flask import Flask, jsonify, render_template
import sys
import os
import json

# Adding the project directory to the Python path to resolve module not found error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cozom.reader import readDatabase
from cozom.models import Symptom, Condition, BodyPart  # Importing relevant classes

app = Flask(__name__)

# Initialize variables for holding the data
data = None
body_parts = []
symptoms = []
conditions = []

# Function to load body parts data
def load_body_parts():
    with open('data/body_parts.json', 'r') as f:
        return json.load(f)

# Function to load symptoms data
def load_symptoms():
    symptoms_list = []
    symptoms_folder = os.path.join('data', 'symptoms')
    for symptom_file in os.listdir(symptoms_folder):
        if symptom_file.endswith('.json'):
            with open(os.path.join(symptoms_folder, symptom_file), 'r') as f:
                symptom = json.load(f)
                symptoms_list.append(symptom)
    return symptoms_list

# Function to load conditions data
def load_conditions():
    conditions_list = []
    conditions_folder = os.path.join('data', 'conditions')
    for condition_file in os.listdir(conditions_folder):
        if condition_file.endswith('.json'):
            with open(os.path.join(conditions_folder, condition_file), 'r') as f:
                condition = json.load(f)
                conditions_list.append(condition)
    return conditions_list

# Loading the data when the app starts
@app.before_first_request
def load_data():
    global body_parts, symptoms, conditions
    body_parts = load_body_parts()
    symptoms = load_symptoms()
    conditions = load_conditions()

# Route to display the home page
@app.route('/')
def home():
    return render_template('about.html')  # Adjusted to render the about page initially

# Route for Symptom Checker
@app.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html', symptoms=symptoms, body_parts=body_parts)

# Route for Body Map
@app.route('/body-map')
def body_map():
    return render_template('BODY MAP HTML/bodymap.html', body_parts=body_parts)

# Route for Diagnosis page
@app.route('/diagnosis')
def diagnosis():
    return render_template('Component HTML/diagnosepage.html')  # Adjusted to the correct component

# Route for the Body Part page
@app.route('/body-part')
def body_part():
    return render_template('Component HTML/bodypart_component.html')  # Adjusted to the correct component

# Route for Condition page
@app.route('/condition')
def condition():
    return render_template('Component HTML/condition_component.html')

# Route for the helpers page
@app.route('/helpers')
def helpers():
    return render_template('helpers.html')

# Route for Structure page
@app.route('/structure')
def structure():
    return render_template('structure.html')

# Route for Image Toggle Front Back page
@app.route('/image-toggle')
def image_toggle():
    return render_template('IMAGE HTML/ImageToggleFrontBack.html')

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
