# Python program to read image using OpenCV 
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/cv2/python-3.7')
# importing OpenCV(cv2) module 
import cv2
# Save image in set directory 
# Read RGB image 
img = cv2.imread('opencv-text-recognition/images/example_06.png')  
  
# Output img with window name as 'image' 
cv2.imshow('image', img)  
  
# Maintain output window utill 
# user presses a key 
cv2.waitKey(0)         
  
# Destroying present windows on screen 
cv2.destroyAllWindows()  