from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from dealio.resources.ocr import extract_from_ktp_image, extract_from_ktp_url

main_route = "/api/vision/v1"

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(extract_from_ktp_image, main_route+"/extract/from-ktp-image")
api.add_resource(extract_from_ktp_url, main_route+"/extract/from-ktp-url")