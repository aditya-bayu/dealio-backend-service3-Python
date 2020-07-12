import cv2
import numpy as np

from dealio.util.point_warp import for_point_warp


def blurring(src):
  gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
  # plt.imshow(gray, cmap="gray")
  # plt.show()
  blur = cv2.GaussianBlur(gray, (3,3), 0)
  # plt.imshow(blur, cmap="gray")
  # plt.show()
  return blur


def auto_canny(image, sigma=0.4):
  # compute the median of the single channel pixel intensities
  v = np.median(image)
  v = 100
  # apply automatic Canny edge detection using the computed median
  lower = int(max(0, (1.0 - sigma) * v))
  upper = int(min(255, (1.0 + sigma) * v))
  edged = cv2.Canny(image, lower, upper)
  # return the edged image
  return edged


def detect_boundary_point(canny) -> list:
  contours, _ = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

  our_cnt = []

  for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)
#    print(len(approx))
#    our_cnt.append(approx)
    if len(approx) == 4:
      our_cnt.append(approx)
  return our_cnt


def transform_wrap_image(image, boundary_point):
  gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
  return for_point_warp(boundary_point[0], gray)