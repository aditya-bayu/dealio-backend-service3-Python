import requests
from flask import request
from flask_restful import Resource
from io import BytesIO

from PIL import Image
import numpy as np
import cv2
import pytesseract

from dealio.util.preprocessing import request_to_array
from dealio.util.tools import blurring, auto_canny, detect_boundary_point, transform_wrap_image
from dealio.util.extract import extraction_KTP_from_ocr


class extract_from_ktp_link(Resource):
  def post(self):
    try:
      URL = request.args.get("link")

      req = requests.get(URL)
      img = Image.open(BytesIO(req.content))
      print(type(img))
    except Exception as e:
      return {
        "message": "Internal Server Error",
        "error": str(e)}, 500


class extract_from_ktp_image(Resource):
  def post(self):
    try:
      filestr = request.files["image"]
      img_rgb = request_to_array(filestr, mode="rgb")

      blur = blurring(img_rgb)
      canny = auto_canny(blur)
      point_boundary = detect_boundary_point(canny)
      if len(point_boundary) == 0:
        # return {"message": "cannot detect boundaries"}, 400
        wrap_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
      else:
        wrap_img = transform_wrap_image(img_rgb, point_boundary)

      text_ocr = pytesseract.image_to_string(wrap_img)
      ocr_exctraction_data = extraction_KTP_from_ocr(text_ocr)

      return {
        "message": "OK",
        "data": ocr_exctraction_data}, 200
    except Exception as e:
      return {
        "message": "Internal Server Error",
        "error": str(e)}, 500