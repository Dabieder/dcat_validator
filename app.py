from flask import Flask, jsonify, request, send_from_directory
import os
from rdflib import Graph
from pyshacl import validate

app = Flask(__name__, static_url_path='/static')

# Directory for SHACL files
SHAPES_DIR = "shapes"


@app.route("/")
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route("/validate", methods=["POST"])
def validate_rdf():
    data = request.get_json()

    return jsonify({
            "conforms": False,
            "validationReport": "Here will be the validation report"
        })