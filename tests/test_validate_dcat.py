import os
import requests
from pyshacl.rdfutil import load_from_source
from rdflib import Graph
from validation.validate_dcat import validate_rdf


def test_vocab_import():
    SHAPES_DIR = "shapes"
    vocab_graph = os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")
    g = load_from_source(vocab_graph, do_owl_imports=True)
    print(g.serialize(format="ttl"))
    assert isinstance(g, Graph)
    # add assertions for sample statements the imported graph should contain


def test_validate_rdf():
    SHAPES_DIR = "shapes"
    VALIDATION_FILES = ["dcat-ap_2.1.1_shacl_shapes.ttl",
                        "dcat-ap-konventionen.ttl",
                        "dcat-ap-spec-german-additions.ttl",
                        "dcat-ap-spec-german-messages.ttl"]
    VOCABULARY_FILE = "dcat-ap-de-imports.ttl"

    url = "https://www.govdata.de/ckan/dataset/supermarkte.rdf"
    filename = url.split("/")[-1]
    filepath = f"./{filename}"

    with open(filepath, "wb") as f:  # write/truncate, binary mode
        content = requests.get(url, stream=True).content
        f.write(content)  # writing / testing temporary file is probably unneccessary

    data_graphs = {"url": url,
                   "file": filepath,  # writing / testing temporary file is probably unneccessary
                   "text": content}

    shacl_graph = Graph()
    for shape_file in VALIDATION_FILES:
        shacl_graph.parse(os.path.join(SHAPES_DIR, shape_file))

    ont_graph = os.path.join(SHAPES_DIR, VOCABULARY_FILE)

    for label, data_graph in data_graphs.items():
        print(f"Testing '{label}':")

        conforms, result = validate_rdf(data_graph, shacl_graph, ont_graph)
        print(conforms, result)
        assert conforms is False

    os.remove(filepath)
