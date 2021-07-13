import numpy as np
import cv2

#img = cv2.imread('apple.jpg')
img2 = cv2.imread('messi5.jpg')
#img3 = cv2.imread('opencv-logo-white.png')

print(img2.shape)
print(img2.size)
print(img2.dtype)
BGR = cv2.split(img2)
img2 = cv2.merge((BGR))

ball = img2[280:340, 330:390]
img2[273:333, 100:160] = ball

#img = cv2. resize(img, (500, 500))
#img3 = cv2.resize(img3, (500, 500))
#dst = cv2.addWeighted(img, .7, img3, .5, 0)

cv2.imshow('image', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()