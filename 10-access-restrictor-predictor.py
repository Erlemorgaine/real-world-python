import os
from datetime import datetime
import cv2 as cv

names = {1: "Monfils"}

root_dir = os.path.abspath('.')

# haarfilters_path = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/'
# facehaar = requests.get(haarfilters_path + 'haarcascade_frontalface_default.xml')
# open('haarcascade_frontalface_default.xml', 'wb').write(facehaar.content)
face_detector = cv.CascadeClassifier(root_dir + '/haarcascade_frontalface_default.xml')

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('lbph_trainer.yml')

test_path = './tester'
image_paths = [os.path.join(test_path, file) for file in os.listdir(test_path)]

# Get faces of test images

for index, image in enumerate(image_paths):
    predict_image = cv.imread(image, cv.IMREAD_GRAYSCALE)
    faces = face_detector.detectMultiScale(predict_image, scaleFactor = 1.05, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(f"Access requested at {datetime.now()}")
        face = cv.resize(predict_image[y:y+h, x:x+w], (100,100))

        # Get the id that the test image is supposed to match with, and the distance with which it matches.
        # The larger the distances, the less the test image resembles the target id person
        predicted_id, dist = recognizer.predict(face)

        if predicted_id == 1 and dist <= 80:
            name = names[predicted_id]
            print("{} identified as {} with distance={}\n".format(image, name, round(dist, 1)))
        else:
            name = 'unnknown'
            print(f"{image} is {name}")

        cv.rectangle(predict_image, (x, y), (x + w, y + h), 255, 2)
        cv.putText(predict_image, name, (x + 1, y + h - 5), cv.FONT_HERSHEY_COMPLEX, 0.5, 255, 1)
        cv.imwrite('PREDICTED_' + str(name) + '_' + str(index) + '.jpg', predict_image[y:y+h, x:x+w])
        cv.destroyAllWindows()