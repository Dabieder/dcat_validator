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
                                        inference=None,
                                        advanced=True,
                                        debug=False)

    return conforms, result_text
