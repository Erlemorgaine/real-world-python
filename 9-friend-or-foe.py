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
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

root_dir = os.path.abspath('.')
# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'

# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# eyehaar = requests.get(haarfilters_path + 'haarcascade_eye.xml')

# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
# open('haarcascade_eye.xml', 'wb').write(eyehaar.content)

face_cascade = cv.CascadeClassifier(root_dir + 'haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier(root_dir + 'haarcascade_eye.xml')

os.chdir('corridor_5')
contents = sorted(os.listdir())



