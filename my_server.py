from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from objectdetect import read as objectdetect

app = Flask(__name__)
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'] )
@cross_origin(origin='*')
def root():
    return {"Welcome To": "Baby And Todder Safety!"}

@app.route('/objectdetect', methods=['POST'] )
@cross_origin(origin='*')
def objectdetect_process():
    # Đọc ảnh từ client gửi lên
    images = request.form.get('images')
    # nhan dien doi tuong
    object_detect = objectdetect(images)

    return object_detect

# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')