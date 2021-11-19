import cv2
import numpy as np
import convertbase64toimage as cvbi


def read(image):
    image =cvbi.convert(image)
    print(image)
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
            if confidence > 0.5:
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
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        data +=str({"id":class_ids[i],"x": round(x),"y": round(y),"xw": round(x + w),"yh": round(y + h)})
    if not data:
       return {"message":"Not Found"}

    return data

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

