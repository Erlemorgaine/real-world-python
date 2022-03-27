import cv2 as cv
import os
import requests
import random
import time

root_dir = os.path.abspath('.')
haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'

# the alt frontalface has higher precision than the default one (used in the sentry gun exercise)
facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_alt.xml')

open('haarcascade_frontalface_alt.xml', 'wb').write(facehaar.content)

face_cascade = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_alt.xml')

# You have to pass the VideoCapture the index of the video device you want to use.
# If you only have one device, the index should be 0.
capture = cv.VideoCapture(0)

while True:
    # This is to load the video frames. The first argument is a Boolean return code, we don't need it.
    # (It's used to check if you've run out of frames when reading from a video file)
    _, frame = capture.read()

    # This scales the frame to 0.5, to optimise the program if necessary
    # cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)

    face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3)

    # BUT the classifiers only detect upright faces! So they often don't recognise my face.
    # To fix this, you can tilt the frames slightly. Or I guess I should use other classifiers??
    for (x, y, w, h) in face_rects:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
        cv.imwrite(f'face_frame.png', frame)

    # cv.imwrite(f'face_frame_{random.random()}.png', frame)

    # This waits for a key press and breaks the program if the press happens
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# This frees up the camera for other applications
capture.release()
cv.destroyAllWindows()