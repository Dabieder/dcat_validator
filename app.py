import os
from flask import Flask, jsonify, request, send_from_directory
from validation.validate_dcat import validate_rdf

app = Flask(__name__, static_url_path="/static")

# Directory for SHACL files
SHAPES_DIR = "shapes"

ALLOWED_EXTENSIONS = {".ttl", ".rdf", ".json"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/validate/url", methods=["POST"])
def validate_from_url():
    print("Received request to validate from URL")

    request_json = request.get_json()

    if "url" not in request_json:
        print("No URL provided")
        return jsonify({"error": "No URL provided"}), 400

    data_graph = request_json["url"]
    shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap_2.1.1_shacl_shapes.ttl")
    ont_graph = None  # os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")

    conforms, result_text = validate_rdf(data_graph, shacl_graph, ont_graph)

    return jsonify({"conforms": conforms, "validationReport": result_text})


@app.route("/validate/file", methods=["POST"])
def validate_file():
    print("Received request to validate file")

    if "file" not in request.files:
        print("No file provided")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file is None or file.filename is None or file.filename == "":
        print("No file selected")
        return jsonify({"error": "No file selected"}), 400

    # check if the file has an allowed extension
    if not allowed_file(file.filename):
        print("Invalid file extension", file.filename)
        return jsonify({"error": "Invalid file extension"}), 400

    if file:
        data_graph = file
        shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap_2.1.1_shacl_shapes.ttl")
        ont_graph = None  # os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")

        conforms, result_text = validate_rdf(data_graph, shacl_graph, ont_graph)

        return jsonify({"conforms": conforms, "validationReport": result_text})

    return jsonify({"error": "An error occurred while processing the file"}), 500


@app.route("/validate/text", methods=["POST"])
def validate():
    print("Received request to validate")

    request_json = request.get_json()

    if "rdf" not in request_json:
        print("No RDF data provided")
        return jsonify({"error": "No RDF data provided"}), 400

    data_graph = request_json["rdf"]
    shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap_2.1.1_shacl_shapes.ttl")
    ont_graph = None  # os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")

    conforms, result_text = validate_rdf(data_graph, shacl_graph, ont_graph)

    return jsonify({"conforms": conforms, "validationReport": result_text})
