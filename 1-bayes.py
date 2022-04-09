import sys 
import random
import itertools
import numpy as np
import cv2 as cv

MAP_FILE = 'cape_python.sepng'

SEARCH_AREA_1_CORNERS = (130, 265, 180, 315) # Indicate area upper left and lower right corner coords
SEARCH_AREA_2_CORNERS = (80, 255, 130, 305)
SEARCH_AREA_3_CORNERS = (105, 205, 155, 255)

class SearchMission():
    def __init__(self, name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)

        if self.img is None:
            print(f'Could not load map file {MAP_FILE}')
            sys.exit(1)

        self.area_actual = 0 # Nr search area
        self.sailor_actual = [0, 0] # Coords within search area of sailor's location when found
        self.search_area_1 = self.img[SEARCH_AREA_1_CORNERS[1] : SEARCH_AREA_1_CORNERS[3], SEARCH_AREA_1_CORNERS[0] : SEARCH_AREA_1_CORNERS[2]]
        self.search_area_2 = self.img[SEARCH_AREA_2_CORNERS[1] : SEARCH_AREA_2_CORNERS[3], SEARCH_AREA_2_CORNERS[0] : SEARCH_AREA_2_CORNERS[2]]
        self.search_area_3 = self.img[SEARCH_AREA_3_CORNERS[1] : SEARCH_AREA_3_CORNERS[3], SEARCH_AREA_3_CORNERS[0] : SEARCH_AREA_3_CORNERS[2]]

        # Probabilities of finding sailor in each area
        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        # Search Effectiveness Probability for each area,
        # i.e. how much of an area you have searched.
        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0


