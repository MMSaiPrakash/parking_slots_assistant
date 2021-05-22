import urllib
import cv2
import numpy as np
import time
from firebase import firebase
firebase = firebase.FirebaseApplication('https://snaggingparking-default-rtdb.firebaseio.com/')
#Change the firebase url to yours and use this code.

url = 'http://192.168.0.109:8080/shot.jpg'  #Change this IP with your Camera's IP
#cap = cv2.VideoCapture(0)
            
freeframe1=0
freeframe3=0
freeframe5=0
freeframe7=0
freeframe2=0
freeframe4=0
freeframe6=0
freeframe8=0

while(1):

    free1 = False
    free3 = False
    free5 = False
    free7 = False
    free2 = False
    free4 = False
    free6 = False
    free8 = False

    #IPCam
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgNp,-1)
    frame=cv2.resize(frame,None,fx=0.5,fy=0.5)

    #LapCam
    #ret, frame = cap.read()

    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray_img, 5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,120,
                               param1=100,param2=30,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            if i[2]<70 and i[2]>50:                
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.putText(frame, str(i[0])+','+str(i[1]),
                            (int(i[0]+i[2]),int(i[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0,0,0), 2, cv2.LINE_AA)
                print i[0],i[1]
                time.sleep(0.1)

####Configure the values of i[0], i[1] and i[2] (x,y and radius) using your
####camera at a fixed distance from the parking spcace


                
            if i[1]>70 and i[1]<100:
                if i[0]<80 and i[0]>50:
                    free1 = True
                    print '1 is available'
                    firebase.put('/SLOT','P1','available')
                if i[0]<170 and i[0]>140:
                    free3 = True
                    print '3 is available'
                    firebase.put('/SLOT','P3','available')
                if i[0]<255 and i[0]>220:
                    free5 = True
                    print '5 is available'
                    firebase.put('/SLOT','P5','available')
                if i[0]<350 and i[0]>310:
                    free7 = True
                    print '7 is available'
                    firebase.put('/SLOT','P7','available')
            elif i[1]<310 and i[1]>270:
                if i[0]<80 and i[0]>50:
                    free2 = True
                    print '2 is available'
                    firebase.put('/SLOT','P2','available')
                if i[0]<170 and i[0]>140:
                    free4 = True
                    print '4 is available'
                    firebase.put('/SLOT','P4','available')
                if i[0]<255 and i[0]>220:
                    free6 = True
                    print '6 is available'
                    firebase.put('/SLOT','P6','available')
                if i[0]<350 and i[0]>310:
                    free8 = True
                    print '8 is available'
                    firebase.put('/SLOT','P8','available')

            if free1==False:
                freeframe1 += 1
            else:
                freeframe1=0
            if free3==False:
                freeframe3 += 1
            else:
                freeframe3=0
            if free5==False:
                freeframe5 += 1
            else:
                freeframe5=0
            if free7==False:
                freeframe7 += 1
            else:
                freeframe7=0
            if free2==False:
                freeframe2 += 1
            else:
                freeframe2=0
            if free4==False:
                freeframe4 += 1
            else:
                freeframe4=0
            if free6==False:
                freeframe6 += 1
            else:
                freeframe6=0
            if free8==False:
                freeframe8 += 1
            else:
                freeframe8=0

            if freeframe1>20:
                print '1 is occupied'
                firebase.put('/SLOT','P1','occupied')
                cv2.circle(frame,(65,85),36,(0,0,255),3)
            if freeframe3>20:
                print '3 is occupied'
                firebase.put('/SLOT','P3','occupied')
                cv2.circle(frame,(155,85),36,(0,0,255),3)
            if freeframe5>20:
                print '5 is occupied'
                firebase.put('/SLOT','P5','occupied')
                cv2.circle(frame,(240,85),36,(0,0,255),3)
            if freeframe7>20:
                print '7 is occupied'
                firebase.put('/SLOT','P7','occupied')
                cv2.circle(frame,(330,85),36,(0,0,255),3)
            if freeframe2>20:
                print '2 is occupied'
                firebase.put('/SLOT','P2','occupied')
                cv2.circle(frame,(65,290),36,(0,0,255),3)
            if freeframe4>20:
                print '4 is occupied'
                firebase.put('/SLOT','P4','occupied')
                cv2.circle(frame,(155,290),36,(0,0,255),3)
            if freeframe6>20:
                print '6 is occupied'
                firebase.put('/SLOT','P6','occupied')
                cv2.circle(frame,(240,290),36,(0,0,255),3)
            if freeframe8>20:
                print '8 is occupied'
                cv2.circle(frame,(330,290),36,(0,0,255),3)
                firebase.put('/SLOT','P8','occupied')
                
    cv2.imshow("Output", frame)
    k=cv2.waitKey(10) & 0xFF
    if k==27:
        break
cv2.destroyAllWindows()
#cap.release()
