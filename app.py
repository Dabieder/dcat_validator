import os
from flask import Flask, jsonify, request, send_from_directory
from validation.validate_dcat import validate_rdf

app = Flask(__name__, static_url_path="/static")

# Directory for SHACL files
SHAPES_DIR = "shapes"

VALIDATION_FILE = "dcat-ap_2.1.1_shacl_shapes.ttl"

ALLOWED_EXTENSIONS = {"ttl", "rdf", "json"}


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

    shacl_graph = get_shacl_graph()
    conforms, result_text = perform_validation(url, shacl_graph)

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

        shacl_graph = get_shacl_graph()
        conforms, result_text = perform_validation(file_content, shacl_graph, data_graph_format=file_extension)

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

    shacl_graph = get_shacl_graph()
    conforms, result_text = perform_validation(rdf_data, shacl_graph)

    return jsonify({"conforms": conforms, "validationReport": result_text})


def perform_validation(
    data_graph, shacl_graph=None, ont_graph=None, data_graph_format: str = "xml"
):
    if shacl_graph is None:
        shacl_graph = os.path.join(SHAPES_DIR, VALIDATION_FILE)

    conforms, result_text = validate_rdf(data_graph, shacl_graph, ont_graph, data_graph_format)
    return conforms, result_text


def get_shacl_graph():
    return os.path.join(SHAPES_DIR, VALIDATION_FILE)
