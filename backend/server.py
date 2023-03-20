import logging
import uuid
from pathlib import Path
from time import sleep
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.skalierungsmethoden.bicubic_interpolation import BicubicInterpolation
from backend.skalierungsmethoden.lanczos_interpolation import LanczosInterpolation
from backend.skalierungsmethoden.pixel_verdopplung import PixelVerdopplung
from backend.skalierungsmethoden.bilinear_interpolation import BilinearInterpolation


app = FastAPI(debug=True)

# configure CORS middleware
origins = ["*"]  # change this to restrict access to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    # return main.html
    return FileResponse("./frontend/main.html")


@app.get("/favicon.ico")
def read_root():
    # return main.html
    return FileResponse("./frontend/favicon.ico")


@app.get("/main.js")
def read_main_js():
    # return main.js
    return FileResponse("./frontend/main.js")


@app.get("/img")
async def read_image(path: str):
    image_path = Path(f"./img/{path}")
    logging.info(f"image file: {image_path}")
    if image_path.is_absolute() or str(image_path).startswith(".."):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    logging.info(f"Serving image file: {image_path}")
    return FileResponse(str(image_path))


@app.post("/img")
async def create_upload_file(file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=422, detail="Only image files are allowed", headers={"X-Error": "Only image files are allowed"})

    if width < 1 or height < 1:
        raise HTTPException(
            status_code=422,
            detail="Resolution must be greater than 0",
            headers={"X-Error": "Resolution must be greater than 0"}
        )

    filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    filepath = f"./img/{filename}"

    try:
        contents = file.file.read()
        with open(filepath, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="",
            headers={"X-Error": "Resolution must be greater than 0"}
        )
    finally:
        file.file.close()

    sleep(1)

    try:
        image_p2 = PixelVerdopplung(filepath).manipulate((width, height))
    except Exception:
        image_p2 = "ALAAARM.png"

    try:
        image_biLi = BilinearInterpolation(filepath).manipulate((width, height))
    except Exception:
        image_biLi = "ALAAARM.png"

    try:
        image_biCu = BicubicInterpolation(filepath).manipulate((width, height))
    except Exception:
        image_biCu = "ALAAARM.png"

    try:
        image_lcz = LanczosInterpolation(filepath).manipulate((width, height))
    except Exception:
        image_lcz = "ALAAARM.png"

    results = [
        {
            "title": "Nearest Neighbor",
            "alt": "Image processed with Nearest Neighbor algorithm",
            "src": f"img?path={image_p2}"
        },
        {
            "title": "Bilinear",
            "alt": "Image processed with Bilinear algorithm",
            "src": f"img?path={image_biLi}"
        },
        {
            "title": "Bicubic",
            "alt": "Image processed with Bicubic algorithm",
            "src": f"img?path={image_biCu}"
        },
        {
            "title": "Lanczos",
            "alt": "Image processed with Lanczos algorithm",
            "src": f"img?path={image_lcz}"
        },
    ]

    return results
