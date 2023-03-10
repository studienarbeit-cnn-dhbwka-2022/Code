from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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
    image_path = f"./img/{path}"
    return FileResponse(image_path)


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

    return {"message": f"Successfully uploaded {file.filename}"}
