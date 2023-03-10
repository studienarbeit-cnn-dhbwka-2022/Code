import logging
from pathlib import Path
from time import sleep
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

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

    try:
        contents = file.file.read()
        with open(f"./img/{file.filename}", 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    sleep(1)

    return {"src": f"http://127.0.0.1:8000/img?path={file.filename}"}
