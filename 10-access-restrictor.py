import os
import numpy as np
import cv2 as cv

root_dir = os.path.abspath('.')

# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'
# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
face_cascade = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_default.xml')

train_path = './trainer'
image_paths= [os.path.join(train_path, file) for file in os.listdir(train_path)]
images, labels = [], []

for image in image_paths:
    train_image = cv.imread(image, cv.IMREAD_GRAYSCALE)

    # Get img filename on first split, get label / user name / frame number on second split
    label = int(os.path.split(image)[-1].split('.')[1])
    name = os.path.split(image)[-1].split('.')[0]
    frame_num = os.path.split(image)[-1].split('.')[2]

    faces = face_cascade.detectMultiScale(train_image)

    for (x, y, w, h) in faces:
        images.append(label)