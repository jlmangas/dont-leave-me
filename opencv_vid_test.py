# opencv_vid_test.py

import numpy as np
import cv2
import time

# If you are having trouble with exceptions when calling detectMultiScale
# you may want to ensure that this path is valid
haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
haar_cascade_profile = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture(0)

while not cap.isOpened():
    pass

while(True):
    # capture frame by frame
    frame_ok, frame = cap.read()
    if not frame_ok:
        print("bad frame")
        continue

    # input("Enter...")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # operation on the frame ...
    # print("trying face detection")
    # If you are having trouble with exceptions when calling detectMultiScale
    # you may want to ensure the file passed to the
    # CascaseClassifier constructor is valid and at the specified location
    face_rects = haar_cascade_face.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for (x,y,w,h) in face_rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (168, 201, 97), 2)
    face_rects = haar_cascade_profile.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for (x,y,w,h) in face_rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (83, 85, 226), 2)

    #display captured frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when done, release capture and close window
cap.release()
cv2.destroyAllWindows()
