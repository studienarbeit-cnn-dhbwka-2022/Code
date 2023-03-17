
const widthInput = document.querySelector('input[aria-label="width"]');
const heightInput = document.querySelector('input[aria-label="height"]');
const output = document.getElementById('output');
const range = document.querySelector('input[aria-label="range"]');
const rangevalue = document.getElementById('range-value');
const results = document.getElementById('results');

const form = document.querySelector('form');
form.addEventListener('submit', uploadImage);


const loadFile = function (event) {
    event.preventDefault();
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src) // free memory

        // set image dimensions as input placeholders
        widthInput.value = output.naturalWidth;
        heightInput.value = output.naturalHeight;
        range.classList.remove("d-none");
        range.removeAttribute('disabled');
        changerangevalue(1);
    }
}

function onScaleChange() {
    const scale = parseFloat(range.value);
  
    const newWidth = Math.round(output.naturalWidth * scale);
    const newHeight = Math.round(output.naturalHeight * scale);

    output.width = newWidth;
    output.height = newHeight;

    widthInput.value = newWidth;
    heightInput.value = newHeight;

    changerangevalue(range.value);
}
  

function ondimensionchange() {
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);
    const originalWidth = parseInt(widthInput.getAttribute("data-original-value"));
    const originalHeight = parseInt(heightInput.getAttribute("data-original-value"));

    if (width > 0 && height > 0 && originalWidth > 0 && originalHeight > 0) {
        const widthScaleFactor = width / originalWidth;
        const heightScaleFactor = height / originalHeight;
        const scaleFactor = Math.max(widthScaleFactor, heightScaleFactor);
        changerangevalue(scaleFactor.toFixed(2));
    }
}

function changerangevalue(value) {
    range.value = value;
    rangevalue.innerHTML = 'Factor of: x' + value;
}


function uploadImage(event) {
    event.preventDefault();

    console.log("ok")

    results.innerHTML = `
<div class="spinner-border" role="status">
    <span class="visually-hidden">Loading...</span>
</div>`;

    const input = document.querySelector('#imageInput');
    const file = input.files[0];

    const width = widthInput.value;
    const height = heightInput.value;


    const formData = new FormData();
    formData.append('file', file);
    formData.append('width', width);
    formData.append('height', height);

    axios.post('img', formData, {
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
                newChild.classList.add('col-lg-3', 'col-md-6', 'position-relative');

                const newTitle = document.createElement('h2');
                newTitle.classList.add('pt-3');
                newTitle.textContent = image.title;

                const newImage = document.createElement('img');
                newImage.src = image.src;
                newImage.classList.add('img-fluid', 'rounded-1', 'shadow');
                newImage.alt = image.alt;

                const htmlAnchorElement = document.createElement('a');
                htmlAnchorElement.classList.add('stretched-link');
                htmlAnchorElement.target = '_blank';
                htmlAnchorElement.href = image.src;


                newChild.appendChild(newTitle);
                newChild.appendChild(newImage);
                newChild.appendChild(htmlAnchorElement);

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


