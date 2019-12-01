from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
import os
import pytesseract
from PIL import Image
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
import json
data={}
count=0

directory = 'Originals/'
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".jpeg") or filename.endswith(".jpg"):
        fn=os.path.join(directory, filename)
        image = cv2.imread(fn)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height = 500)
        
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        #mt = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #edged = cv2.Canny(th3, 75, 200)
         
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
        print(len(approx))

        
        if len(approx)==4:
            count=count+1
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
            warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

            # convert the warped image to grayscale, then threshold it
            # to give it that 'black and white' paper effect
            warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            T = threshold_local(warped, 11, offset = 10, method = "gaussian")
            warped = (warped > T).astype("uint8") * 255
            img_p=imutils.resize(warped, height = 600)
            deno=cv2.fastNlMeansDenoising(img_p,None,9,13)
            cv2.imwrite("Processed/"+filename,deno)
            im_pil=Image.open("Processed/"+filename)
            text = pytesseract.image_to_string(im_pil)
            # print("STEP 1: Edge Detection")
            #cv2.imshow("Image", image)
            data[filename]=text
            print(filename)
            print(text)
            img_or=Image.open(fn)
            img_or.show()
            im_pil.show()
            n=input("(1):")
            # cv2.imshow("Edged",deno)
            # # #cv2.
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

    else:
        continue
print(count)
with open('data.txt', 'w') as json_file:
  json.dump(data, json_file)

# # find the contours in the edged image, keeping only the
# # largest ones, and initialize the screen contour
# cnts = cv2.findContours(th3.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# # loop over the contours
# for c in cnts:
#     # approximate the contour
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
#     # if our approximated contour has four points, then we
#     # can assume that we have found our screen
#     if len(approx) == 4:
#         screenCnt = approx
#         break
# screenCnt = approx
# print(len(approx))

# show the contour (outline) of the piece of paper
# print("STEP 2: Find contours of paper")

# # # apply the four point transform to obtain a top-down
# # # view of the original image
# warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
 
# # convert the warped image to grayscale, then threshold it
# # to give it that 'black and white' paper effect
# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = (warped > T).astype("uint8") * 255
 
# # show the original and scanned images
# print("STEP 3: Apply perspective transform")
# #cv2.imshow("Original", imutils.resize(orig, height = 650))
# cv2.imshow("Scanned", imutils.resize(warped, height = 650))
# cv2.waitKey(0)
