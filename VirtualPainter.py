import cv2
import numpy as np
import time
import os
import HandTrackinMin as htm


############################

xp,yp =0,0

###########################
folderPath = "Headers"
myList = os.listdir(folderPath)
print(myList)
color = (255, 255,255)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.HandTracking(detectionCon=0.85)

imgCanvas = np.zeros((720,1280,3),np.uint8)
while True:



    # 1. Import image
    success, img = cap.read()


    img2 = img
    img = cv2.flip(img,1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)

    if len(lmList) != 0:
        #print(lmList)

        # tip of index and middle fingers
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]



    # 3. Check which fingers are up

        fingers = detector.fingersUp()
        #print(fingers)
    # 4. If Selection mode - Twfo finger up



        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255),cv2.FILLED)
            print("Selection Mode")
            if y1<125:
                if 250<x1<450:
                    header = overlayList[0]
                    color = (147, 20, 255)

                elif 550<x1<750:
                    header = overlayList[1]
                    color = (255, 0, 0)
                elif 800<x1<950:
                    header = overlayList[2]
                    color = (0, 255, 0)
                elif 1050<x1<1200:
                    header = overlayList[3]
                    img[y1 - 15:y1 + 15, x1 - 15:x1 + 15] = img2[y1 - 15:y1 + 15, x1 - 15:x1 + 15]
                    color = (0, 0, 0)

        if fingers[1] and fingers[2]==False:

            #cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)

            if xp==0 and yp==0:
                xp,yp = x1,y1


            cv2.line(img,(xp,yp),(x1,y1),color,15)
            cv2.circle(imgCanvas,(xp,yp),15,color,-1)

            print("Drawing Mode")

            xp,yp = x1,y1
    # 5. If Drawing Mode - Index finger is up



    # Setting the header image
    img[0:125,0:1280] = header
    cv2.imshow("Image",cv2.bitwise_or(img,imgCanvas))
    cv2.waitKey(1)
