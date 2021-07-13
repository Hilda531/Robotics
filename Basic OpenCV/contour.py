import cv2

img = cv2.imread('opencv-logo.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = " + str(len(contours)))
print(contours[0])

cv2.drawContours(img, contours, -1, (50, 50, 150), 3)

cv2.imshow('gambar', img)
cv2.imshow('abuabu', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()