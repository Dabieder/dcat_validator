from pyshacl import validate
from pyshacl.rdfutil import load_from_source, mix_graphs
from rdflib import Graph


def validate_rdf(data_graph: str, shacl_graph: str, ont_graph: str, data_graph_format: str = "xml"):

    if not isinstance(data_graph, Graph):
        original_data_graph = load_from_source(data_graph, do_owl_imports=False)

    if not isinstance(ont_graph, Graph):
        ont_graph = load_from_source(ont_graph, do_owl_imports=True)

    # we merge ont_graph and data_graph beforehand, because validate()
    # only merges OWL and RDFS statements, we need SKOS statements
    data_graph = mix_graphs(original_data_graph, ont_graph)

    conforms, _, result_text = validate(data_graph,
                                        data_graph_format=data_graph_format,
                                        shacl_graph=shacl_graph,
                                        shacl_graph_format="ttl",
                                        ont_graph=None,
                                        ont_graph_format=None,
                                        do_owl_imports=True,
                                        inference=None,
                                        advanced=True,
                                        debug=False)

    return conforms, result_text
