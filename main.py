from fastapi import FastAPI
import objectdetect as od

app = FastAPI()
@app.post('/objectdetect')
def objectdetect(hinhanh: str):
    object_detect = od.read(hinhanh)
    return object_detect

@app.get("/")
def read_root():
    return {"Hello": "World"}
