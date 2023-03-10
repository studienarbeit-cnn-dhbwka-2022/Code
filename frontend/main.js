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

    const results = document.getElementById('results');
    results.innerHTML = `
<div class="spinner-border" role="status">
    <span class="visually-hidden">Loading...</span>
</div>`;

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
            console.log(response.data.length);
            results.innerHTML = '';

            for (let i = 0; i < response.data.length; i++) {
                const image = response.data[i];

                const newChild = document.createElement('div');
                newChild.classList.add('col-lg-3', 'col-sm-6');

                const newTitle = document.createElement('h2');
                newTitle.classList.add('pt-3');
                newTitle.textContent = image.title;

                const newImage = document.createElement('img');
                newImage.src = image.src;
                newImage.classList.add('img-fluid', 'rounded-1');
                newImage.alt = image.alt;

                newChild.appendChild(newTitle);
                newChild.appendChild(newImage);

                results.appendChild(newChild);
            }
        })
        .catch(error => {
            console.error(error);
            results.innerHTML = `
<div class="row justify-content-md-center">
    <div class="col col-lg-6 p-3 bg-danger rounded-3 text-white" id="error">
        <p>Fehler beim Laden der Datei!</p>
        <p>Bitte versuchen Sie es erneut.</p>
        <p>Fehler: ${error} </p>
    </div>
</div>
`
        });
}


