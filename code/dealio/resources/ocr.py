import requests
from flask import request
from flask_restful import Resource
from io import BytesIO

from PIL import Image
import numpy as np
import cv2
import pytesseract

from dealio.util.preprocessing import request_to_array
from dealio.util.extract import extraction_KTP_from_ocr, ocr_from_array


class extract_from_ktp_url(Resource):
  def post(self):
    try:
      mode = request.args.get("mode") or "prod"
      json = request.get_json()
      URL = json.get("url")

      req = requests.get(URL)
      img_rgb = Image.open(BytesIO(req.content))
      img_rgb = np.asarray(img_rgb)

      text_ocr = ocr_from_array(img_rgb)
      ocr_exctraction_data = extraction_KTP_from_ocr(text_ocr)

      data = {"ktp": ocr_exctraction_data}
      if mode == "debug":
        data["ocr"] = text_ocr

      return {
        "message": "OK",
        "data": data}, 200

    except Exception as e:
      return {
        "message": "Internal Server Error",
        "error": str(e)}, 500


class extract_from_ktp_image(Resource):
  def post(self):
    try:
      mode = request.args.get("mode") or "prod"

      filestr = request.files["image"]
      img_rgb = request_to_array(filestr, mode="rgb")

      text_ocr = ocr_from_array(img_rgb)
      ocr_exctraction_data = extraction_KTP_from_ocr(text_ocr)
      
      data = {"ktp": ocr_exctraction_data}
      if mode == "debug":
        data["ocr"] = text_ocr

      return {
        "message": "OK",
        "data": data}, 200
    except Exception as e:
      return {
        "message": "Internal Server Error",
        "error": str(e)}, 500