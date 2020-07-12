import numpy as np
import cv2
import pytesseract

def request_to_array(request_file, mode="rgb"):
  npimg = np.fromfile(request_file, np.uint8)
  img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
  if mode == "rgb":
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  elif mode == "gray":
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  else:
    return