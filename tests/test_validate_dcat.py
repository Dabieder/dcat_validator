from validation.validate_dcat import validate_rdf

def test_validate_rdf():
    validation_result = validate_rdf("rdf_data", "shape_file")
    assert validation_result == True