const loadFile = function (event) {
    event.preventDefault();

    const output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src) // free memory
    }
}

const element = document.querySelector('form');
element.addEventListener('submit', event => {
    event.preventDefault();
    // actual logic, e.g. validate the form
    console.log('Form submission cancelled.');

    const input = document.getElementById("imageInput");
    const file = input.files[0];
    if (!file) {
        alert("Please select an image file.");
        return;
    }
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // The response text is the URL of the processed image
                const imageUrl = xhr.responseText;
                // Update the placeholder image with the processed image
                const placeholderImage = document.getElementById("out");
                placeholderImage.src = imageUrl;
            } else {
                alert("An error occurred while processing the image.");
            }
        }
    };
    xhr.open("POST", "http://127.0.0.1:8000/img");
    xhr.setRequestHeader("Content-Type", "application/octet-stream");
    xhr.send(file);
})


