from fastapi import FastAPI
import objectdetect as od

app = FastAPI()

@app.post('/objectdetect')
async def objectdetect(images: str):
    object_detect = od.read(images)
    return object_detect

@app.get("/")
def read_root():
    return {"Hello": "World"}
