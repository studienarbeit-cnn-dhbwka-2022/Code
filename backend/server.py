import logging
from pathlib import Path
from time import sleep
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.skalierungsmethoden.pixel_verdopplung import PixelVerdopplung

app = FastAPI()

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
async def create_upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=422, detail="Only image files are allowed")

    filepath = f"./img/{file.filename}"

    try:
        contents = file.file.read()
        with open(filepath, 'wb') as f:
            f.write(contents)
    except Exception:
        return {
            "message": "There was an error uploading the file",
            "error": f"{Exception}",
        }
    finally:
        file.file.close()

    sleep(1)

    try:
        PixelVerdopplung(filepath).manipulate((200, 200))
    except:
        pass

    results = [
        {
            "title": "Nearest Neighbor",
            "alt": "Image processed with Nearest Neighbor algorithm",
            "src": f"img?path={file.filename}"
        },
        {
            "title": "Bilinear",
            "alt": "Image processed with Bilinear algorithm",
            "src": f"img?path={file.filename}"
        },
        {
            "title": "Bicubic",
            "alt": "Image processed with Bicubic algorithm",
            "src": f"img?path={file.filename}"
        },
        {
            "title": "Lanczos",
            "alt": "Image processed with Lanczos algorithm",
            "src": f"img?path={file.filename}"
        },
    ]

    return results
