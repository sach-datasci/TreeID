from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import uvicorn
import tensorflow as tf
from tensorflow.keras.models import load_model
import model
import os
import uuid
import preprocessing

app = FastAPI()

# Mount the static directory to serve CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

loaded_model = load_model('siamesemodel_gray_cnn.h5', 
                         custom_objects={'L1Dist':model.L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})

# Render the index.html file
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/{name}')
def get_name(name:str):
    return{'message':f'Hello,{name} Sir.'}

INPUT_PATH = 'database/input_img'
RAW_IMG_PATH = 'database/temp'
DATASET_PATH = 'database/dataset'

@app.post('/upload')
async def upload_img(file_name: str = Form(...), file: UploadFile = File(...)):
    print(f"Received file_name: {file_name}, file: {file.filename}")
    # Rest of your code...
    file.filename=f"{file_name}.jpg"
    content = await file.read()
    file_path = f"{RAW_IMG_PATH}/{file.filename}"
    with open(file_path,'wb') as f:
        f.write(content)
    preprocessing.process_images_in_folder(RAW_IMG_PATH, DATASET_PATH, output_size=(200, 200), min_contour_area=5000)
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(f"{INPUT_PATH}/{file.filename}"):
        os.remove(f"{INPUT_PATH}/{file.filename}")
    return {"filename":file.filename}

@app.post('/verify')
async def verify_img(file: UploadFile=File(...)):
    file.filename=f"{uuid.uuid4()}.jpg"
    content = await file.read()
    file_path = f"{RAW_IMG_PATH}/{file.filename}"
    with open(file_path,'wb') as f:
        f.write(content)
    preprocessing.process_images_in_folder(RAW_IMG_PATH, INPUT_PATH, output_size=(200, 200), min_contour_area=5000)
    str_tree = model.verify(loaded_model, file.filename, 0.5)
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(f"{INPUT_PATH}/{file.filename}"):
        os.remove(f"{INPUT_PATH}/{file.filename}")
    return {"tree_str": str_tree}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)