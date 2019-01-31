# opencv_vid_test.py

import numpy as np
import cv2
import os
from time import sleep
from twilio.rest import Client


# If you are having trouble with exceptions when calling detectMultiScale
# you may want to ensure that this path is valid
haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def capture_frame(cap):
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

    return frame, len(face_rects)

def publish_frame():
    os.system('git commit test.jpg -m \"x\"')
    os.system('git push')
    sleep(3) # wait some time for push to be good


def send_message():
    # --- Twilio setup ---
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC76d3438864cb9d1cff0db5e7408f7b0f'
    auth_token = '53560a5bf72bc414dac02c643de9d88c'
    client = Client(account_sid, auth_token)

    # send a twilio message
    message = client.messages.create(
            body='You forgot your Baby in the car fam fam!',
            from_='+14846962393',
            media_url='https://raw.githubusercontent.com/jlmangas/dont-leave-me/master/test.jpg',
            to='+12486655960'
        )
    return

def main():
    # --- initialize video capture ---
    cap = cv2.VideoCapture(0)

    while not cap.isOpened():
        pass

    # --- main loop ---
    while(True):
        frame, n_faces = capture_frame(cap)

        #display captured frame
        cv2.imshow('frame', frame)

        # wait 100 ms for a key press - this also controls the loop period (sort of)
        k = cv2.waitKey(50)    # -1 means no key pressed
        if (k & 0xFF) == ord('q'):
            break
        if (k & 0xFF) == ord('+'):
            print("*** checking for occupants ...")
            if (n_faces > 0):
                print("   !!! occupants left in cabin - sending notice")
                cv2.imwrite('test.jpg', frame)
                sleep(0.1)  # wait for write to complete
                publish_frame()
                # send a twilio message
                send_message()
            else:
                print("   ... cabin is vacant - OK to park")

    # when done, release capture and close window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
