const API_BASE_URL = 'http://127.0.0.1:8000';

// Function to upload image
async function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName').value;
    const file = fileInput.files[0];
    const uploadSpinner = document.getElementById('uploadSpinner');
    const uploadButton = document.querySelector('.primary-btn');

    if (!fileName || !file) {
        alert('Please provide both file name and select an image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_name', fileName); // Use 'file_name' to match the backend

    uploadButton.disabled = true; // Disable button
    uploadButton.style.display = 'none'; // Hide button
    uploadSpinner.style.display = 'inline-block'; // Show spinner

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        document.getElementById('uploadResponse').innerHTML = `File uploaded: ${data.filename}`;
    } catch (error) {
        document.getElementById('uploadResponse').innerHTML = 'Error uploading file.';
        console.error('Error:', error);
    } finally {
        uploadButton.style.display = 'block'; // Show button again
        uploadButton.disabled = false; // Enable button
        uploadSpinner.style.display = 'none'; // Hide spinner
    }
}

// Function to verify image
async function verifyImage() {
    const verifyInput = document.getElementById('verifyInput');
    const file = verifyInput.files[0];
    const verifySpinner = document.getElementById('verifySpinner');
    const verifyButton = document.querySelector('.secondary-btn');

    if (!file) {
        alert('Please select an image to verify.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    verifyButton.disabled = true; // Disable button
    verifyButton.style.display = 'none'; // Hide button
    verifySpinner.style.display = 'inline-block'; // Show spinner

    try {
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        document.getElementById('verifyResponse').innerHTML = `Verification Result: ${data.tree_str}`;
    } catch (error) {
        document.getElementById('verifyResponse').innerHTML = 'Error verifying file.';
        console.error('Error:', error);
    } finally {
        verifyButton.style.display = 'block'; // Show button again
        verifyButton.disabled = false; // Enable button
        verifySpinner.style.display = 'none'; // Hide spinner
    }
}