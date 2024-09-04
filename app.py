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

    data_graph = request_json["rdf"]
    shacl_graph = os.path.join(SHAPES_DIR, "dcat-hvd.ttl")

    validation_result = validate_rdf(data_graph, shacl_graph)

    return jsonify(validation_result)
