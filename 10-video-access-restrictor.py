import os
from datetime import datetime
import cv2 as cv

names = {1: "Monfils"}

root_dir = os.path.abspath('.')

names = {1: "Monfils"}


# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'
# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
face_detector = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_default.xml')

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('lbph_trainer.yml')

# You have to pass the VideoCapture the index of the video device you want to use.
# If you only have one device, the index should be 0.
capture = cv.VideoCapture(0)

# Get faces of test images

while True:
    # This is to load the video frames. The first argument is a Boolean return code, we don't need it.
    # (It's used to check if you've run out of frames when reading from a video file)
    _, frame = capture.read()
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # This scales the frame to 0.5, to optimise the program if necessary
    # cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)

    face_rects = face_detector.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3)

    # BUT the classifiers only detect upright faces! So they often don't recognise my face.
    # To fix this, you can tilt the frames slightly. Or I guess I should use other classifiers??
    for (x, y, w, h) in face_rects:
        face = cv.resize(gray_img[y:y+h, x:x+w], (100,100))

        # Get the id that the test image is supposed to match with, and the distance with which it matches.
        # The larger the distances, the less the test image resembles the target id person
        predicted_id, dist = recognizer.predict(face)

        if predicted_id == 1 and dist <= 80:
            name = names[predicted_id]
        else:
            name = 'unknown'
        cv.rectangle(gray_img, (x, y), (x+w, y+h), (255, 255, 255), 2)
        cv.putText(gray_img, name, (x + 1, y + h - 5), cv.FONT_HERSHEY_COMPLEX, 1, 255, 1)
        cv.imwrite(f'ACCESS_face_frame.png', gray_img)

    # cv.imwrite(f'face_frame_{random.random()}.png', frame)

    # This waits for a key press and breaks the program if the press happens
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# This frees up the camera for other applications
capture.release()
cv.destroyAllWindows()
