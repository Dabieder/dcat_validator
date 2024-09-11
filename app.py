import os
from rdflib import Graph
from flask import Flask, jsonify, request, send_from_directory
from validation.validate_dcat import validate_rdf

app = Flask(__name__, static_url_path="/static")

# Directory for SHACL files
SHAPES_DIR = "shapes"

VALIDATION_FILES = ["dcat-ap_2.1.1_shacl_shapes.ttl",
                    "dcat-ap-konventionen.ttl",
                    "dcat-ap-spec-german-additions.ttl",
                    "dcat-ap-spec-german-messages.ttl"]

VOCABULARY_FILE = "dcat-ap-de-imports.ttl"

ALLOWED_EXTENSIONS = {"ttl", "rdf", "json", "xml"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/validate/url", methods=["POST"])
def validate_from_url():
    print("Received request to validate from URL")

    request_json = request.get_json()

    url = request_json["url"]

    if not url:
        print("No URL provided")
        return jsonify({"error": "No URL provided"}), 400

    conforms, result_text = perform_validation(url)

    return jsonify({"conforms": conforms, "validationReport": result_text})


@app.route("/validate/file", methods=["POST"])
def validate_file():
    print("Received request to validate file")

    if "rdf_file" not in request.files:
        print("No file provided")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["rdf_file"]

    # check if the file has an allowed extension
    if file is None or file.filename == "" or not allowed_file(file.filename):
        print("Invalid file or extension", file.filename)
        return jsonify({"error": "Invalid file extension"}), 400

    try:
        file_extension = file.filename.rsplit(".", 1)[1].lower()
        file_content = file.read().decode("utf-8")

        conforms, result_text = perform_validation(file_content, data_graph_format=file_extension)

        return jsonify({"conforms": conforms, "validationReport": result_text})

    except Exception as e:
        return jsonify({"error": "An error occurred while processing the file"}), 500


@app.route("/validate/text", methods=["POST"])
def validate():
    print("Received request to validate")

    request_json = request.get_json()
    rdf_data = request_json.get("rdf")

    if not rdf_data:
        print("No RDF data provided")
        return jsonify({"error": "No RDF data provided"}), 400

    conforms, result_text = perform_validation(rdf_data)

    return jsonify({"conforms": conforms, "validationReport": result_text})


def perform_validation(
    data_graph, shacl_graph=None, ont_graph=None, data_graph_format: str = "xml"
):
    if shacl_graph is None:
        shacl_graph = get_shacl_graph()

    if ont_graph is None:
        ont_graph = get_ont_graph()

    conforms, result_text = validate_rdf(data_graph, shacl_graph, ont_graph, data_graph_format)
    return conforms, result_text


def get_shacl_graph():
    shacl_graph = Graph()
    for shape_file in VALIDATION_FILES:
        shacl_graph.parse(os.path.join(SHAPES_DIR, shape_file))
    return shacl_graph


def get_ont_graph():
    return os.path.join(SHAPES_DIR, VOCABULARY_FILE)
