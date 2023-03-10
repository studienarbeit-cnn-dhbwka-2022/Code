const loadFile = function (event) {
    event.preventDefault();

    const output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src) // free memory
    }
}

const form = document.querySelector('form');
form.addEventListener('submit', uploadImage);

function uploadImage(event) {
    event.preventDefault();

    const input = document.querySelector('#imageInput');
    const file = input.files[0];

    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://127.0.0.1:8000/img', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(response => {
            console.log(response.data.src)

            const results = document.getElementById('results');

            const newChild = document.createElement('div');
            newChild.classList.add('col-lg-3', 'col-sm-6');

            const newTitle = document.createElement('h2');
            newTitle.classList.add('pt-3');
            newTitle.textContent = response.data.src.title;

            const newImage = document.createElement('img');
            newImage.src = response.data.src;
            newImage.classList.add('img-fluid', 'rounded-1');
            newImage.alt = response.data.src.alt;

            newChild.appendChild(newTitle);
            newChild.appendChild(newImage);

            results.appendChild(newChild);

            // The response text is the URL of the processed image
            const imageUrl = response.data.src;
            // Update the placeholder image with the processed image
            const placeholderImage = document.getElementById("out");
            placeholderImage.src = imageUrl;
        })
        .catch(error => {
            console.error(error);
        });
}


