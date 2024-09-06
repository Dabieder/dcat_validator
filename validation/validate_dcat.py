import os
import requests
from pyshacl import validate


def validate_rdf(data_graph: str, shacl_graph: str, ont_graph: str):

    print(f"{data_graph}")
    conforms, _, result_text = validate(data_graph,
                                        data_graph_format="xml",
                                        shacl_graph=shacl_graph,
                                        shacl_graph_format="ttl",
                                        ont_graph=ont_graph,
                                        ont_graph_format="ttl",
                                        do_owl_imports=True,
                                        inference="rdfs",
                                        advanced=True,
                                        debug=False)

    return conforms, result_text


# Testing
SHAPES_DIR = "shapes"

url = "https://www.govdata.de/ckan/dataset/supermarkte.rdf"
filename = url.split("/")[-1]
filepath = f"./validation/{filename}"

with open(filepath, "wb") as f:  # write/truncate, binary mode
    content = requests.get(url, stream=True).content
    f.write(content)

data_graphs = {"url": url,
               "file": filepath,
               "text": content}

shacl_graph = os.path.join(SHAPES_DIR, "dcat-ap_2.1.1_shacl_shapes.ttl")
ont_graph = None  # os.path.join(SHAPES_DIR, "dcat-ap-de-imports.ttl")

for label, data_graph in data_graphs.items():
    print(f"Testing '{label}':")
    conforms, result = validate_rdf(data_graph, shacl_graph, ont_graph)
    print(conforms, result)
