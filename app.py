from flask import Flask, jsonify, request, send_from_directory
import os
from rdflib import Graph
from .validation.validate_dcat import validate_rdf

app = Flask(__name__, static_url_path='/static')

# Directory for SHACL files
SHAPES_DIR = "shapes"


@app.route("/")
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route("/validate", methods=["POST"])
def validate():
    request_json = request.get_json()

    rdf_data = request_json["rdf"]

    validation_result = validate_rdf(rdf_data, os.path.join(SHAPES_DIR, "dcat-hvd.ttl"))

    return jsonify({
            "conforms": False,
            "validationReport": "Alles super"
        })