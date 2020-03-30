import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/cv2/python-3.7')
import cv2
import numpy as np
from PIL import Image
import pytesseract


# from picamera import PiCamera
# from time import sleep

# camera = PiCamera()

# camera.start_preview()
# sleep(5)
# camera.capture('/home/pi/Desktop/image2.jpg')
# camera.stop_preview()




# img = cv2.imread('/home/pi/Desktop/image2.jpg')
# img = cv2.imread('images/example_06.png')
img = cv2.imread('example_06.png')
cv2.imshow('image', img)
gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel=np.ones((3,3),np.uint8)
gray= cv2.erode(img,kernel,iterations=1)
cv2.imshow('gray', gray)


text = pytesseract.image_to_string(gray,lang="eng")
print(text)


cv2.waitKey(0)
cv2.destroyAllWindows()

