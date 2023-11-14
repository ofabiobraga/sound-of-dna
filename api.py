from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated, Union
from pathlib import Path
from sonification import Sonification
import shutil
import time
import json

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.mount("/static", StaticFiles(directory="static"), name="static")


@api.get('/')
async def index():
    return FileResponse('static/index.html')

@api.post('/')
async def post(
    file: Annotated[UploadFile, File()],
    scale: Annotated[Union[str, None], Form()] = None,
    bmp: Annotated[Union[str, None], Form()] = None,
    instruments: Annotated[Union[str, None], Form()] = None,
    strategies: Annotated[Union[str, None], Form()] = None
    ):
    
    # Checks if the 'uploads' directory exists.
    Path('uploads').mkdir(parents=True, exist_ok=True)
    
    # Defines where the uploaded file will be stored.
    filename = str(time.time()) + '-' + file.filename
    filepath = './uploads/' + filename
    
    # Stores uploaded file.
    with open(filepath, "wb") as uploaded_file:
        shutil.copyfileobj(file.file, uploaded_file)
    
    if bmp is not None:
        bmp = int(bmp)
        
    if instruments is not None:
        instruments = json.loads(instruments)
        
    if strategies is not None:
        strategies = json.loads(strategies)

    # Gets sonification data.
    sonification = Sonification(
        filepath,
        scale,
        bmp,
        instruments,
        strategies
    )

    response = sonification.process()

    return response

@api.get('/{type}/{filename}')
async def midi(type:str, filename: str):
    # Defines where the uploaded file will be stored.
    filepath = './' + type + '/' + filename

    if not Path(filepath).is_file():
        raise HTTPException(status_code=404, detail="File does not exist! " + filepath)

    return FileResponse(filepath, headers={"Content-Disposition": f"attachment; filename={filename}"})
