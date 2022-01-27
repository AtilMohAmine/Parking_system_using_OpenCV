import cv2
import pickle
import numpy

#load the list of parking places if exist
try:
    with open('ParkingPos', 'rb') as f:
        placeList = pickle.load(f)
except:
    placeList = []

#the size of the parking box
width, height = 110, 45

#load the video file
cap = cv2.VideoCapture('demo.mp4')

def checkParkingPlace(imgDilate):
    freePlaces = 0

    for place in placeList:
        x, y = place
        imgCrop = imgDilate[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
        if count < 900:
            color = (0, 255, 0)
            freePlaces += 1
        else:
            color = (0, 0, 255)
 
        cv2.rectangle(img, place, (place[0] + width, place[1] + height), color, 3)
        cv2.putText(img, str(count), place, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)

    cv2.putText(img, 'Available: '+str(freePlaces), (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        placeList.append((x, y))     
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(placeList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                placeList.pop(i)

    with open('ParkingPos', 'wb') as f:
        pickle.dump(placeList, f)          

while True:
    success, img = cap.read()
    #make video replay
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    #set image color to black and white
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = numpy.ones((3, 3), numpy.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingPlace(imgDilate)

    cv2.imshow("Parking System", img)
    cv2.setMouseCallback("Parking System", mouseClick)
    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()