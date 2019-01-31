# opencv_vid_test.py

import numpy as np
import cv2
import os
from time import sleep
from twilio.rest import Client

# --- Twilio setup ---
# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC76d3438864cb9d1cff0db5e7408f7b0f'
auth_token = '53560a5bf72bc414dac02c643de9d88c'
client = Client(account_sid, auth_token)


# If you are having trouble with exceptions when calling detectMultiScale
# you may want to ensure that this path is valid
haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#haar_cascade_profile = cv2.CascadeClassifier('haarcascade_profileface.xml')

cap = cv2.VideoCapture(0)

while not cap.isOpened():
    pass

while(True):
    # capture frame by frame
    frame_ok, frame = cap.read()

    # haar cascades require grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # operation on the frame ...
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

    if len(face_rects):
        cv2.imwrite('test.jpg', frame)
        sleep(0.1)  # wait for write to complete
        os.system('git commit test.jpg -m \"x\"')
        os.system('git push')
        sleep(1) # wait some time for push to be good
        # send a twilio message
        message = client.messages.create(
                body='You forgot your Baby in the car fam fam!',
                from_='+14846962393',
                media_url='https://raw.githubusercontent.com/jlmangas/dont-leave-me/master/test.jpg',
                to='+12486655960'
            )
        break

    # Profile detection
    # face_rects = haar_cascade_profile.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=5,
    #     minSize=(30, 30)
    # )
    # for (x,y,w,h) in face_rects:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (83, 85, 226), 2)

    #display captured frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when done, release capture and close window
cap.release()
cv2.destroyAllWindows()
