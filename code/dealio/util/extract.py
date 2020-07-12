import numpy as np
import cv2
import pytesseract

from dealio.util.preprocessing import request_to_array
from dealio.util.tools import blurring, auto_canny, detect_boundary_point, transform_wrap_image
from dealio.util.matcher import (
  find_nik_value, 
  find_name_value,
  find_dob_value,
  find_gender_value)

def extraction_KTP_from_ocr(ocr_string:str) -> dict:
  result = dict()

  rows = ocr_string.split("\n")
  for idx, row in enumerate(rows):
    nik = find_nik_value(row)
    nama = find_name_value(row)
    dob = find_dob_value(row)
    gender = find_gender_value(row)
    
    if nik:
      result["nik"] = nik
    if nama:
      result["name"] = nama 
    if dob:
      result["dob"] = dob
    if gender:
      result["gender"] = gender

  # get attribute by rows
  if result.get("nik") is None:
    try:
      result["nik"] = rows[3]
    except:
      pass

  if result.get("name") is None:
    try:
      result["name"] = rows[5]
    except:
      pass

  if result.get("dob") is None:
    try:
      result["dob"] = rows[6]
    except:
      pass

  if result.get("gender") is None:
    try:
      result["gender"] = rows[7]
    except:
      pass

  return result


def ocr_from_array(img_rgb:np.ndarray) -> str:
  blur = blurring(img_rgb)
  canny = auto_canny(blur)
  point_boundary = detect_boundary_point(canny)
  if len(point_boundary) == 0:
    # return {"message": "cannot detect boundaries"}, 400
    wrap_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
  else:
    wrap_img = transform_wrap_image(img_rgb, point_boundary)

  return pytesseract.image_to_string(wrap_img)