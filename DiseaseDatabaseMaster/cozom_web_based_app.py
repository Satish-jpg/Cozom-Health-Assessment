from flask import Flask, jsonify, render_template, abort, url_for
import sys
import os
import json
import logging

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cozom.reader import readDatabase
from cozom.models import Symptom, Condition, BodyPart

# Initialize Flask app with dynamic paths for templates and static files
current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, "templates"),
    static_folder=os.path.join(current_dir, "static"),
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = app.logger

# Data folder path (dynamic for local and deployed environments)
DATA_FOLDER = os.getenv("DATA_FOLDER", os.path.join(current_dir, "data"))

# Required templates and static files
required_templates = [
    "404.html", "about.html", "bodypart.html", "conditions.html", "details.html",
    "diagnosis.html", "helpers.html", "info.html", "questions.html",
    "structure.html", "symptom.html", "symptom_checker.html",
    "BODY MAP HTML/bodymap.html", "Component HTML/aboutpage.html",
    "Component HTML/bodypart_component.html", "Component HTML/condition_component.html",
    "Component HTML/diagnosepage.html", "Component HTML/symptom_component.html",
    "IMAGE HTML/ImageToggleFrontBack.html"
]

required_static_files = {
    "CSS": ["404.css", "about.css", "bodypart.css", "conditions.css", "details.css",
            "diagnosis.css", "helpers.css", "info.css", "questions.css", "symptom.css",
            "BODY MAP CSS/bodymap.css", "Component CSS/aboutpage.css",
            "Component CSS/bodypart_component.css", "Component CSS/condition_component.css",
            "Component CSS/diagnosepage.css", "Component CSS/symptom_component.css",
            "IMAGE CSS/background-image.css"],
    "js": ["404.js", "about.js", "bodypart.js", "conditions.js", "details.js",
           "diagnosis.js", "helpers.js", "symptom.js", "JavaScriptToggle.js",
           "BODY MAP JS/bodymap.js", "COMPONENT JS/aboutpage.js",
           "COMPONENT JS/bodypart_component.js", "COMPONENT JS/condition_component.js",
           "COMPONENT JS/diagnosepage.js", "COMPONENT JS/symptom_component.js"]
}

# Verify templates
def verify_templates():
    """Checks if all required templates exist."""
    missing_templates = []
    for template in required_templates:
        template_path = os.path.join(app.template_folder, template.replace("/", os.sep))
        if not os.path.exists(template_path):
            missing_templates.append(template)
    if missing_templates:
        logger.error(f"Missing templates: {missing_templates}")
        return False
    logger.info("All templates verified.")
    return True

# Verify static files
def verify_static_files():
    """Checks if all required static files exist."""
    missing_files = []
    for folder, files in required_static_files.items():
        for file in files:
            static_file_path = os.path.join(app.static_folder, folder.replace("/", os.sep), file)
            if not os.path.exists(static_file_path):
                missing_files.append(f"{folder}/{file}")
    if missing_files:
        logger.error(f"Missing static files: {missing_files}")
        return False
    logger.info("All static files verified.")
    return True

if not verify_templates() or not verify_static_files():
    sys.exit("Application cannot start due to missing templates or static files.")

# Helper function to load JSON files safely
def load_json_file(filepath):
    """Load JSON file with error handling."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None

# Data loading functions
def load_body_parts():
    """Load body parts data."""
    parts_file = os.path.join(DATA_FOLDER, 'body_parts.json')
    return load_json_file(parts_file) or []

def load_symptoms():
    """Load symptoms data."""
    symptoms_folder = os.path.join(DATA_FOLDER, 'symptoms')
    if not os.path.exists(symptoms_folder):
        logger.warning(f"Symptoms folder not found: {symptoms_folder}")
        return []
    return [
        load_json_file(os.path.join(symptoms_folder, file))
        for file in os.listdir(symptoms_folder) if file.endswith('.json')
    ]

def load_conditions():
    """Load conditions data."""
    conditions = []
    for folder_name in ['conditions_part1', 'conditions_part2']:
        folder = os.path.join(DATA_FOLDER, folder_name)
        if not os.path.exists(folder):
            logger.warning(f"Conditions folder not found: {folder}")
            continue
        conditions += [
            load_json_file(os.path.join(folder, file))
            for file in os.listdir(folder) if file.endswith('.json')
        ]
    return conditions

# Load data once at application start
logger.info("Loading data...")
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
    app.run(debug=True, host='0.0.0.0', port=5001)
