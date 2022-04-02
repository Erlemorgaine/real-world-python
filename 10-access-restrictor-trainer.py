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

    # Get img filename 
    filename = os.path.split(image)[-1]
    
    # get label / user name / frame number 
    # Label corresponds to the user id input
    label = int(filename.split('.')[1])
    name = filename.split('.')[0]
    frame_num = filename.split('.')[2]

    faces = face_cascade.detectMultiScale(train_image)

    for (x, y, w, h) in faces:
        images.append(train_image[y:y+h, x:x+w])
        labels.append(label)
        print(f"Preparing training images for {filename}")

        # cv.imshow('Training img', train_image[y:y+h, x:x+w])
        cv.waitKey(50)
    
cv.destroyAllWindows()

# This Local Binary Patterns Histogram algorithm uses a filter of 3x3 with ones and zeroes
# to check if the surrounding pixels have a value higher than the pixel in the middle.
# It then converts the resulting binary strings of ones and zeroes to a number, which will be 
# the resulting pixel value.
recogniser = cv.face.LBPHFaceRecognizer_create()

# Labels are my user id for all images of my face (so functions like labeling images in 2 categories as 1 and 0)
recogniser.train(images, np.array(labels))

# Here we create a reusable file for the face recognition data
recogniser.write('lbph_trainer.yml')

print("Training complete. Exiting...")