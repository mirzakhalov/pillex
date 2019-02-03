import cv2 as cv
import numpy as np


class Enhancer:


    def __init__(self):
        print("initialized")


    def enhance(self,filepath):
        alpha = 1.0
        # read the image
        image = cv.imread(filepath)
        if image is None:
            print('Could not open or find the image: ', args.input)
            exit(0)
        
        # change the contrast of the image by manipulating the alpha value
        new_image = cv.convertScaleAbs(image, alpha=alpha, beta=20)
        cv.imwrite(filepath + ".jpg",new_image)
        return filepath
    

    
    
