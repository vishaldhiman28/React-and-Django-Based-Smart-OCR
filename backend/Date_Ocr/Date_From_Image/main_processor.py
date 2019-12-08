from .transform import four_point_transform
import numpy as np
import cv2
import imutils
import os
import pytesseract
from PIL import Image
from pytesseract import Output
import re

regular_exp=[r'(\d+/\d+/\d+)',r'(\d+-\d+-\d+)']

def process_image(input_image):
    image = cv2.imread(input_image)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
     
    #show the original image and the edge detected image
    cnts = cv2.findContours(th3.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
     
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    screenCnt = approx


    if len(approx)==4:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        warped = cv2.GaussianBlur(warped, (5, 5), 0)
        ret3,warped = cv2.threshold(warped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        warped=cv2.fastNlMeansDenoising(warped,None,9,13)
        img_p=imutils.resize(warped, height = 600)
        deno=cv2.fastNlMeansDenoising(img_p,None,9,13)
        cv2.imwrite(input_image,deno)
        im_pil=Image.open(input_image)
        text = pytesseract.image_to_string(im_pil)
        data_w = pytesseract.image_to_data(im_pil,output_type=Output.DICT)
        n_boxes=len(data_w['level'])
        date_info="NULL"
        for i in range(n_boxes):
        
            for rex_ in regular_exp:
                match = re.search(rex_,data_w['text'][i])
                if match:
                    date_info=match.group()
                    break
        if len(text)==0:
            text="NULL"
        return text,date_info
    else:
        return "NULL","NULL"
