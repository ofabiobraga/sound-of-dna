from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Annotated
from pathlib import Path
from sonification import Sonification
import shutil
import time

api = FastAPI()

@api.post('/')
async def post(file: Annotated[UploadFile, File()]):
    # Checks if the 'uploads' directory exists.
    Path('uploads').mkdir(parents=True, exist_ok=True)
    
    # Defines where the uploaded file will be stored.
    filename = str(time.time()) + '-' + file.filename
    filepath = './uploads/' + filename
    
    # Stores uploaded file.
    with open(filepath, "wb") as uploaded_file:
        shutil.copyfileobj(file.file, uploaded_file)

    # Gets sonification data.
    sonification = Sonification(filepath)
    
    response = sonification.process()

    return response
    
@api.get('/midi/{filename}')
async def midi(filename: str):
    # Defines where the uploaded file will be stored.
    filepath = './midi/' + filename

    if not Path(filepath).is_file():
        raise HTTPException(status_code=404, detail="MIDI file does not exist! " + filepath)

    return FileResponse(filepath, headers={"Content-Disposition": f"attachment; filename={filename}"})
