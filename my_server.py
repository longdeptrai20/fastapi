from fastapi import FastAPI, UploadFile, File
import objectdetect as od

app = FastAPI()
@app.post('/objectdetect')
async def objectdetect(hinhanh: str):
    object_detect = od.read(hinhanh)
    return object_detect
# uvicorn my_server:app
