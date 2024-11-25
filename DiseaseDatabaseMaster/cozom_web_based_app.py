from flask import Flask, jsonify, render_template, abort, url_for
import sys
import os
import json
import logging

# Adding the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cozom.reader import readDatabase
from cozom.models import Symptom, Condition, BodyPart

# Initialize Flask app
app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Templates and static folder paths
templates_path = os.path.join(os.getcwd(), "templates")
static_folder = os.path.join(os.getcwd(), "static")
DATA_FOLDER = r"D:\Cozom"

# Required templates and static files
required_templates = [
    "about.html", "info.html", "questions.html",
    "symptom_checker.html", "conditions.html",
    "details.html", "404.html"
]
required_static_files = {
    "CSS": ["about.css", "404.css", "conditions.css", "details.css"],
    "js": ["about.js", "404.js", "conditions.js", "details.js"]
}

# Verify templates
def verify_templates():
    """Checks if all required templates exist."""
    if not os.path.exists(templates_path):
        logger.error(f"Templates folder not found: {templates_path}")
        return False
    missing_templates = [
        template for template in required_templates
        if not os.path.exists(os.path.join(templates_path, template))
    ]
    if missing_templates:
        logger.error(f"Missing templates: {missing_templates}")
        return False
    logger.info("All templates verified.")
    return True

# Verify static files
def verify_static_files():
    """Checks if all required static files exist."""
    if not os.path.exists(static_folder):
        logger.error(f"Static folder not found: {static_folder}")
        return False
    missing_files = []
    for folder, files in required_static_files.items():
        folder_path = os.path.join(static_folder, folder)
        for file in files:
            if not os.path.exists(os.path.join(folder_path, file)):
                missing_files.append(f"{folder}/{file}")
    if missing_files:
        logger.error(f"Missing static files: {missing_files}")
        return False
    logger.info("All static files verified.")
    return True

if not verify_templates() or not verify_static_files():
    sys.exit("Application cannot start due to missing templates or static files.")

# Initialize global variables for data
body_parts = []
symptoms = []
conditions = []

logger.info(f"Using DATA_FOLDER: {DATA_FOLDER}")

# Helper function to load JSON files safely
def load_json_file(filepath):
    """Load JSON file with error handling."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None

# Load body parts
def load_body_parts():
    """Load body parts data."""
    parts_file = os.path.join(DATA_FOLDER, 'body_parts.json')
    parts_data = load_json_file(parts_file)
    if parts_data:
        return [{"id": int(k), "name": v} for k, v in parts_data.items()]
    logger.warning("Body parts data is empty.")
    return []

# Load symptoms
def load_symptoms():
    """Load symptoms data."""
    symptoms_folder = os.path.join(DATA_FOLDER, 'symptoms')
    if not os.path.exists(symptoms_folder):
        logger.warning(f"Symptoms folder not found: {symptoms_folder}")
        return []
    symptoms = []
    for file in os.listdir(symptoms_folder):
        if file.endswith('.json'):
            symptom_data = load_json_file(os.path.join(symptoms_folder, file))
            if symptom_data:
                symptoms.append(symptom_data)
    return symptoms

# Load conditions
def load_conditions():
    """Load conditions data."""
    conditions = []
    for folder_name in ['conditions_part1', 'conditions_part2']:
        folder = os.path.join(DATA_FOLDER, folder_name)
        if not os.path.exists(folder):
            logger.warning(f"Conditions folder not found: {folder}")
            continue
        for file in os.listdir(folder):
            if file.endswith('.json'):
                condition_data = load_json_file(os.path.join(folder, file))
                if condition_data:
                    conditions.append(condition_data)
    return conditions

# Load data before each request
@app.before_request
def load_data():
    """Load data before each request."""
    global body_parts, symptoms, conditions
    logger.info("Loading body parts, symptoms, and conditions...")
    body_parts = load_body_parts()
    symptoms = load_symptoms()
    conditions = load_conditions()

# Routes
@app.route('/')
def home():
    return render_template('about.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/conditions')
def conditions_view():
    return render_template('conditions.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html', symptoms=symptoms, body_parts=body_parts)

@app.route('/body-part/<int:part_id>')
def detailed_body_part(part_id):
    """Display details for a specific body part."""
    part = next((item for item in body_parts if item["id"] == part_id), None)
    if not part:
        abort(404, description="Body part not found")
    return render_template('bodypart.html', part=part)

@app.route('/helpers')
def helpers():
    return render_template('helpers.html')

@app.route('/structure')
def structure():
    return render_template('structure.html')

@app.route('/image-toggle')
def image_toggle():
    return render_template('IMAGE HTML/ImageToggleFrontBack.html')

@app.route('/component-html/aboutpage')
def about_page_component():
    return render_template('Component HTML/aboutpage.html')

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template('404.html', error=e), 404

if __name__ == "__main__":
    logger.info("Starting Cozom Web App...")
    data = readDatabase(DATA_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5001)
