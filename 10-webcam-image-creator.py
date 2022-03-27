import os
from matplotlib.pyplot import gray
import pyttsx3
import cv2 as cv
from playsound import playsound

engine = pyttsx3.init()

voices = engine.getProperty('voices')
voice = voices[10]

engine.setProperty('rate', 145)
engine.setProperty('volume', 1)
engine.setProperty('voice', voice.id)

root_dir = os.path.abspath('.')
tone_path = os.path.join(root_dir, 'tone.wav')

# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'
# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
face_cascade = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_default.xml')

capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Could not open video device.")

# Set frame width and height
capture.set(3, 640)
capture.set(4, 480)

engine.say('Look directly at the webcam (without glasses on). \
    Make faces with multiple expressions. \
    Continue until you here the tone.')

engine.runAndWait()

name = input("\nEnter last name: \n")
user_id = input("\nEnter user ID: \n")
print("\nCapturing face, look at the camera!")

if not os.path.isdir('trainer'):
    os.mkdir('trainer')
os.chdir('trainer')

frame_count = 0

while True:
    # Capture 30 frames
    _, frame = capture.read()
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    face_rects = face_cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in face_rects:
        frame_count += 1
        # We only save the portion with in the face rectangle, to make sure that 
        # no background features are gonna influence the learning
        cv.imwrite(str(name) + '.' + str(user_id) + '.' + str(frame_count) + '.jpg', gray[x:x+w, y:y+h])
        cv.waitKey(400)
    if frame_count >= 30:
        break

print("\nImage collecrion complete. Exiting...")
playsound(tone_path, block=False)
capture.release()
cv.destroyAllWindows()
