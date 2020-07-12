from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from dealio.resources.ocr import extract_from_ktp_image

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(extract_from_ktp_image, "/extract/from-ktp-image")

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)