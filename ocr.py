from cv2.gapi.streaming import size
import pytesseract
from PIL import Image
import cv2
import numpy as np

#function definitions

# function to get skew angle of an image
def GetSkewAngle(cvImage):

    # add slight blur to reduce noise
    img = cv2.GaussianBlur(cvImage, (9,9), 0)
    ShowImage(img, 'blur')

    # threshold values
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV +
                    cv2.THRESH_OTSU)[1]
    ShowImage(img, 'thresh')
    # expand text fields by dilating white pixels
    # larger kernel on x axis to merge characters
    # smaller kernel on Y axis to separate lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    img = cv2.dilate(img, kernel, iterations=5)
    ShowImage(img, 'dilate')

    # find contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)

    # contours is now sorted by area, so first element is the largest contour
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)

    # determine angle
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

def RotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def DeskewImage(cvImage):
    angle = GetSkewAngle(cvImage)
    return RotateImage(cvImage, angle)

def ShowImage(image, title='image'):
    width = int(image.shape[1] * .2)
    height = int(image.shape[0] * .2)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(title, image)
    #cv2.imshow('Original image', normalImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ocr stuff
#load input image and convert it to RGB

def ExtractText(imagePath):
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # IMAGE PREPROCESSING

    # normalize image
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img = (cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX))

    # grayscale
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # remove noise
    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

    # threshold image
    img = cv2.threshold(img, 105, 255, cv2.THRESH_BINARY)[1]

    # use tesseract to scan an image for text
    text = pytesseract.image_to_string(img)
    print(text)

    return text
