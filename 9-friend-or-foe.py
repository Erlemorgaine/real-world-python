import os
from urllib import request
import requests
import time
from datetime import datetime
from playsound import playsound
import pyttsx3 # This is a text-to-speech library
import cv2 as cv

# Engine is a name by convention
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 145) # Rate of speech
engine.setProperty('volume', 1.0)
engine.setProperty('voice', voices[1])

root_dir = os.path.abspath('.')
tone_path = os.path.join(root_dir, 'tone.wav')
# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'

# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# eyehaar = requests.get(haarfilters_path + 'haarcascade_eye.xml')

# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
# open('haarcascade_eye.xml', 'wb').write(eyehaar.content)

face_cascade = cv.CascadeClassifier(root_dir + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(root_dir + 'haarcascade_eye.xml')

os.chdir('corridor_5')
contents = sorted(os.listdir())

for image in contents:
    print(f"Motion detected at {datetime.now()}")
    discharge_weapon = True
    engine.say("You have entered an active fire zone. \
        Face the machine! \
        You have 5 seconds.")

    # This halts program execution, flushes say() queue and plays the audio
    engine.runAndWait()
    time.sleep(3)

    # This simulates making a capture of the video stream.
    # There is not really a reason to make the image grey, except the author liked to show a grey image.
    # Actually opencv only works with greyscale images, but converts them itself behind the scenes
    img_gray = cv.imread(image, cv.IMREAD_GRAYSCALE)
    height, width = img_gray.shape

    # Showing the image is for quality control, to make sure all the images are being used
    cv.imshow(f'Motion detected {image}', img_gray)
    cv.waitKey(2000)
    cv.destroyWindow(f'Motion detected {image}')

    # The items in this list will be the x, y, width height of the rectangle from the image
    face_rect_list = []
    face_rect_list.append(face_cascade.detectMultiScale(image=img_gray,
        scaleFactor=1.1,
        minNeighbors=5))



