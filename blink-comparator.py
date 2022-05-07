import os
from pathlib import Path
import numpy as np
import cv2 as cv

# These are the points that match between two images. 
# For maximum efficiency better to keep this to the lowest 
# value that still returns good results
MIN_NUM_KEYPOINT_MATCHES = 50

def find_best_matches(img1, img2):
    """Return list of keypoints and list of best matches for two images."""

    # ORB detects and describes keypoints
    orb = cv.ORB_create(nfeatures=100) # Initiate ORB project

    kp1, descriptor_1 = orb.detectAndCompute(img1, mask=None)
    kp2, descriptor_2 = orb.detectAndCompute(img2, mask=None)

    # Find keypoints common to both images
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    matches = bf.match(descriptor_1, descriptor_2)
    #Best matches will have lowest distance value, which is why we want to sort
    matches = sorted(matches, key=lambda x: x.distance)

    best_matches = matches[:MIN_NUM_KEYPOINT_MATCHES]

    return kp1, kp2, best_matches

def main():
    """Loop through 2 folders with paired images (to put on the left and right side), register & blink images"""

    night1_files = sorted(os.listdir('night_1'))
    night2_files = sorted(os.listdir('night_2'))

    path1 = Path.cwd() / 'night_1'
    path2 = Path.cwd() / 'night_2'
    path3 = Path.cwd() / 'night_1_registered' # This will be the output folder

    for i, _ in enumerate(night1_files):
        img1 = cv.imread(str(path1 / night1_files[i]), cv.IMREAD_GRAYSCALE)
        img2 = cv.imread(str(path2 / night2_files[i]), cv.IMREAD_GRAYSCALE)

        print(f"Comparing {night1_files[i]} to {night2_files[i]}.\n")

        # best_matches will be a list of the matching keypoints
        kp1, kp2, best_matches = find_best_matches(img1, img2)

        # Draws the matches on the pictures
        # Output the new drawn-on image to file
        img_match = cv.drawMatches(img1, kp1, img2, kp2, best_matches, outImg=f"{night1_files[i][:-4]}_matches.png")
        height, width = img1.shape
        cv.line(img_match, (width, 0), (width, height), (255, 255, 255), 1)

        # I'm not doing this, since it's literally just a function showing the image on
        # my screen with imshow, which doesn't work on my mac
        # QC_best_matches(img_match) 

        img1_registered = register_image(img1, img2, kp1, kp2, best_matches)

        blink(img1, img1_registered, 'Check registration', num_loops=5)

        out_filename = f"{night1_files[i][:-4]}_registered.png"
        cv.imwrite(str(path3 / out_filename), img1_registered) # This will overwrite a file with the same name
        cv.destroyAllWindows()

        blink(img1_registered, img2, 'Blink comparator', num_loops=15)