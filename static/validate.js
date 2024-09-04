const app = Vue.createApp({
    data() {
        return {
            inputType: 'textarea',  // Default input type is textarea
            rdfText: '',            // Bound to the textarea
            fileName: '',           // Display the uploaded file name
            fileData: null,         // Store the uploaded file data
            rdfUrl: '',             // Bound to the URL input
            output: ''              // Output for validation results
        };
    },
    methods: {
        // Handles file upload and stores the file
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file.name;
                this.fileData = file;  // Store file data for submission
            }
        },

        // Handles the validation logic based on selected input type
        validate() {
            if (this.inputType === 'textarea') {
                this.validateText();
            } else if (this.inputType === 'file') {
                this.validateFile();
            } else if (this.inputType === 'url') {
                this.validateUrl();
            }
        },

        // Validation for text input
        validateText() {
            fetch('/validate/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    rdf: this.rdfText
                }),
            })
            .then(response => response.json())
            .then(data => {
                this.output = `Validation Result: ${data.conforms ? 'Conforms' : 'Does not conform'}\n${data.validationReport}`;
            })
            .catch(error => {
                this.output = `Error during validation: ${error}`;
            });
        },

        // Validation for file upload
        validateFile() {
            const formData = new FormData();
            formData.append('rdf_file', this.fileData);  // Append file to FormData

            fetch('/validate/file', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                this.output = `Validation Result: ${data.conforms ? 'Conforms' : 'Does not conform'}\n${data.validationReport}`;
            })
            .catch(error => {
                this.output = `Error during validation: ${error}`;
            });
        },

        // Validation for URL input
        validateUrl() {
            fetch('/validate/url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: this.rdfUrl
                }),
            })
            .then(response => response.json())
            .then(data => {
                this.output = `Validation Result: ${data.conforms ? 'Conforms' : 'Does not conform'}\n${data.validationReport}`;
            })
            .catch(error => {
                this.output = `Error during validation: ${error}`;
            });
        },

        // Clear the output field
        clearOutput() {
            this.output = '';
        },

        // Clear the input fields
        clearInput() {
            this.rdfText = '';
            this.fileName = '';
            this.fileData = null;
            this.rdfUrl = '';
        }
    }
});

app.mount('#app');
