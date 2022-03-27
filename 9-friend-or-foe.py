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

face_cascade = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(root_dir + '/haarcascade_eye.xml')

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
    # time.sleep(3)

    # This simulates making a capture of the video stream.
    # There is not really a reason to make the image grey, except the author liked to show a grey image.
    # Actually opencv only works with greyscale images, but converts them itself behind the scenes
    img_gray = cv.imread(image, cv.IMREAD_GRAYSCALE)
    height, width = img_gray.shape

    # Showing the image is for quality control, to make sure all the images are being used
    # NB This doesn't work, seems to be a problem with macOS
    # Also NB: after running this the second time, it seems to stop the program
    # cv.imshow(f'Motion detected {image}', img_gray)
    # cv.waitKey(2000)
    # cv.destroyWindow(f'Motion detected {image}')

    # The items in this list will be the x, y, width height of the rectangle from the image
    face_rect_list = []
    face_rect_list.append(face_cascade.detectMultiScale(image=img_gray,
        # scaling is to make sure the input image will be the same size as the ones to train the classifier, 
        # by downscaling it in increments of 10% (e.g. with a factor of 1.2, it increments with 20%)
        scaleFactor=1.1, 
        # The neighbors can be tuned if the algorithm doesn't recognize the faces well enough.
        # It basically detects how many rectangles each rectangle has as neighbors (the more neighbors, the better,
        # since the more features are detected). Increasing this value will increase detection quality 
        # but reduce the number of detections (rectangles on the image)
        minNeighbors=5)) 

    # For a more foolproof system we use also the haar eye features in addition to the frontal face feature
    print(f"Searching for eyes in {image}.")

    for rect in face_rect_list:
        for (x, y, w, h) in rect:
            # Get the face rectangle from the image
            rect_4_eyes = img_gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(image=rect_4_eyes, scaleFactor=1.05, minNeighbors=2)

            for (xEye, yEye, wEye, hEye) in eyes:
                print("Eyes detected.")
                center = (int(xEye + 0.5 * wEye), int(yEye + 0.5 * hEye))
                radius = int((wEye + hEye) / 3)
                # This is for our visual confirmation that an eye is found in this place
                cv.circle(rect_4_eyes, center, radius, 255, 2)
                # Also draw a rectangle on the face
                cv.rectangle(img_gray, (x, y), (x+w, y+h), (255, 255, 255), 2)
                discharge_weapon = False
                break

    

    if discharge_weapon == True:
        cv.putText(img_gray, 'FIRE!', (int(width / 2) - 20, int(height / 2)), cv.FONT_HERSHEY_PLAIN, 3, 255, 3)

    # Because of the bug with imshow and mac, we save the images instead of showing them
    cv.imwrite('PROCESSED_' + image, img_gray)

# The book continues to show 'Fire' on the image when discharge_weapon is True and play the safe-sound if its False