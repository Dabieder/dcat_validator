import os
import requests
from validation.validate_dcat import validate_rdf


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

    shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap_2.1.1_shacl_shapes.ttl")
    ont_graph = None  # os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")

    for label, data_graph in data_graphs.items():
        print(f"Testing '{label}':")
        conforms, result = validate_rdf(data_graph, shacl_graph, ont_graph)
        print(conforms, result)
        assert conforms is False

    os.remove(filepath)
