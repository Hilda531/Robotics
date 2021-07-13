import cv2

vid = cv2.VideoCapture(0);
while True:
    _, frame = vid.read()
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, ',', y)
            font = cv2.FONT_HERSHEY_DUPLEX
            strXY = str(x) + ',' + str(y)
            cv2.putText(vid, strXY, (x, y), font, .5, (50, 250, 255), 1)
            cv2.imshow('image', vid)

    cv2.imshow("frame", frame)
    cv2.setMouseCallback('frame', click_event)
    esc = cv2.waitKey(1)
    if esc == 27:
        break
vid.release()
cv2.destroyAllWindows()