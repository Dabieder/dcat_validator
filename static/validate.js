// Function that runs when clicking the "Validate" button
function validate() {
    let rdfText = document.getElementById("rdfTextarea").value;
    let shaclText = document.getElementById("shaclTextarea").value;
    
    // // Example validation logic
    // if (rdfText === "" || shaclText === "") {
    //     alert("Both RDF and SHACL inputs are required for validation.");
    // } else {
    //     // Placeholder validation logic
    //     alert("Validation in progress...");
    //     // Here you would include actual validation logic
    // }


    fetch('/validate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rdf: rdfText,
            shacl: shaclText
        })
    })
}

// Add event listeners for buttons
window.onload = function() {
    // Validate button
    document.getElementById("validateButton").addEventListener("click", validate);

    // Clear RDF textarea
    document.getElementById("clearRdfButton").addEventListener("click", function() {
        document.getElementById("rdfTextarea").value = "";
    });

    // Clear SHACL textarea
    document.getElementById("clearShaclButton").addEventListener("click", function() {
        document.getElementById("shaclTextarea").value = "";
    });
};
