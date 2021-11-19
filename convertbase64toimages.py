import base64
def convert(imageslink):
    with open(imageslink, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    return b64_string

