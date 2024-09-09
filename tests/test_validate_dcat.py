import os
import requests
from pyshacl.rdfutil import load_from_source, mix_graphs
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

    url = "https://www.govdata.de/ckan/dataset/supermarkte.rdf"
    filename = url.split("/")[-1]
    filepath = f"./{filename}"

    with open(filepath, "wb") as f:  # write/truncate, binary mode
        content = requests.get(url, stream=True).content
        f.write(content)  # writing / testing temporary file is probably unneccessary

    data_graphs = {"url": url,
                   "file": filepath,  # writing / testing temporary file is probably unneccessary
                   "text": content}

    shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap-de.ttl")
    ont_graph = os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")
    ont_graph = load_from_source(ont_graph, do_owl_imports=True)

    for label, data_graph in data_graphs.items():
        print(f"Testing '{label}':")
        if not isinstance(data_graph, Graph):
            original_data_graph = load_from_source(data_graph, do_owl_imports=False)

        data_graph = mix_graphs(original_data_graph, ont_graph)

        conforms, result = validate_rdf(data_graph, shacl_graph, None)
        print(conforms, result)
        assert conforms is False

    os.remove(filepath)
