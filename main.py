from fastapi import FastAPI
import numpy as np
import base64
import cv2

app = FastAPI()

@app.post('/objectdetect')
async def objectdetect(images: str):
    object_detect =read(images)
    return object_detect

@app.get("/")
def read_root():
    return {"Hello": "World"}


import convertbase64toimage as cvbi


def read(image):
    image =convert(image)
    weights_link = 'yolov2-tiny_6000.weights'
    config_link = 'yolov2-tiny .cfg'
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    net = cv2.dnn.readNet(weights_link, config_link)

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.995:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    data = ""
    title="Fire hazard detected: high hazard"
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        data +=str({"id":class_ids[i],"title":title,"x": round(x),"y": round(y),"xw": round(x + w),"yh": round(y + h)})
    if not data:
        title="Fire hazard detected: low hazard"
        data = str({"id": 2, "title": title, "x": 2, "y": 2, "xw": 500, "yh": 500})
    # {"message": "Not Found"}
    return data

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def convert(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64



# uvicorn main:app

