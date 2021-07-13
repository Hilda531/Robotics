import numpy as np
import cv2

gbr = np.zeros([510, 510, 3], np.uint8)

gbr = cv2.line(gbr, (0, 0), (510, 510), (0, 255, 0), 7)
gbr = cv2.arrowedLine(gbr, (0, 255), (255, 0), (180, 240, 7), 5)
gbr = cv2.rectangle(gbr, (255,255), (510,510), (5, 255, 251), 3)
gbr = cv2.circle(gbr, (255,255), 50, (255, 0, 0), -1)
font = cv2.FONT_HERSHEY_COMPLEX
gbr = cv2.putText(gbr, 'HALLOOO', (110, 255), font, 2, (85, 0, 255), 8, cv2.LINE_AA)

cv2.imshow('image', gbr)
cv2.waitKey(0)
cv2.destroyAllWindows()