from fastapi import FastAPI
import objectdetect as od

app = FastAPI()
@app.post('/objectdetect')
async def objectdetect(hinhanh: str):
    object_detect = od.read(hinhanh)
    return object_detect
@app.get("/")
def read_root():
    return {"Hello": "World"}
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
# uvicorn WebService.main:app