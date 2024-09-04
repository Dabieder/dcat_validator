import os
from pyshacl import validate


def validate_rdf(data_graph: str, shacl_graph: str):

    conforms, _, result_text = validate(data_graph,
                                        data_graph_format="ttl",
                                        shacl_graph=shacl_graph,
                                        shacl_graph_format="ttl",
                                        inference="rdfs",
                                        advanced=True,
                                        debug=False)

    return {"conforms": conforms,
            "validationReport": result_text}


# Testing
SHAPES_DIR = "shapes"

data_graph = "https://www.govdata.de/ckan/dataset/supermarkte.rdf"
shacl_graph = os.path.join(SHAPES_DIR, "dcat-hvd.ttl")

result = validate_rdf(data_graph, shacl_graph)

print(result["validationReport"])
