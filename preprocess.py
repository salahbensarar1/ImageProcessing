import cv2
import numpy as np

class Preprocess:
    def __init__(self, img):
        # initialize image
        self.img = img
        # resize image to 80% of original size if image is too large
        if self.img.shape[0] > 600 or self.img.shape[1] > 600:
            self.img = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)

    """
    --- Private Function ---

    Description:
        Preprocess image to detect card
    
    Parameters:
        None

    Returns:
        closing: image after preprocessing

    This function will perform the following:
        1. sharpen image using detailEnhance
        2. convert image to grayscale
        3. blur image using GaussianBlur to remove noise
        4. apply edge detection using Canny
        5. dilate image to fill in holes
        6. close gaps using closing
        7. return closing image
    """
    def __preprocess(self):
        # sharpen image using detailEnhance
        detail = cv2.detailEnhance(self.img, sigma_s=20, sigma_r=0.15)
        # convert image to grayscale
        gray = cv2.cvtColor(detail, cv2.COLOR_BGR2GRAY)
        # blur image using GaussianBlur to remove noise
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        # apply edge detection using Canny
        edge_image = cv2.Canny(blur, 75, 200)
        # Morphological Transform
        kernel = np.ones((10, 10), np.uint8)
        # dilate image to fill in holes
        dilate = cv2.dilate(edge_image, kernel, iterations=1)
        # close gaps using closing
        closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        # return closing image
        return closing
    
    """
    --- Private Function ---

    Description:
        Correct the alignment of the card

    Parameters:
        contours: list of contours

    Returns:
        img: image after correcting alignment

    This function will perform the following:
        1. sort contours by area
        2. get the largest contour
        3. get the bounding rectangle of the largest contour
        4. get the angle of the largest contour
        5. rotate image by the angle
        6. return rotated image 
    """
    def __correct_alignment(self, contours):
        # sort contours by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        # get the largest contour and its bounding rectangle
        x, y, w, h = cv2.boundingRect(contours[0])
        # find the angle of the largest contour
        angle = cv2.minAreaRect(contours[0])[-1]
        # if angle is greater than 45, rotate image by (90 - angle)
        if angle > 45:
            # multiply by -1 to rotate opposite direction
            angle = (90 - angle) * -1
        # find the width and height of the image
        (h, w) = self.img.shape[:2]
        # get the center of the image
        center = (w // 2, h // 2)
        # get rotation matrix
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        # rotate image
        self.img = cv2.warpAffine(self.img, rot_mat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        # return rotated image
        return self.img
    
    """
    --- Public Function ---

    Description:
        Detect card from image and return the card image

    Parameters:
        None

    Returns:
        roi: card image as region of interest

    This function will perform the following:
        1. preprocess image to detect card
        2. find contours
        3. correct alignment of card
        4. sharpen image using detailEnhance
        5. convert image to grayscale
        6. apply edge detection using Canny
        7. dilate image to fill in holes
        8. close gaps using closing
        9. find contours
        10. sort contours by area
        11. get the largest contour
        12. get the bounding rectangle of the largest contour
        13. crop image using the bounding rectangle
        14. return cropped image
    """
    def detect_card_from_image(self):
        # preprocess image to detect card
        closing = self.__preprocess()
        # find contours
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # correct alignment of card
        self.img = self.__correct_alignment(contours)
        # sharpen image using detailEnhance
        detail = cv2.detailEnhance(self.img, sigma_s=20, sigma_r=0.15)
        # convert image to grayscale
        gray = cv2.cvtColor(detail, cv2.COLOR_BGR2GRAY)
        # apply edge detection using Canny
        edge_image = cv2.Canny(gray, 75, 200)
        # Morphological Transform
        kernel = np.ones((10, 10), np.uint8)
        # dilate image to fill in holes
        dilate = cv2.dilate(edge_image, kernel, iterations=1)
        # close gaps using closing
        closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        # find contours
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # sort contours by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        # get the largest contour and its bounding rectangle
        x, y, w, h = cv2.boundingRect(contours[0])
        # crop image using the bounding rectangle
        roi = self.img[y:y+h, x:x+w]
        # sharpen image
        laplacian = cv2.Laplacian(self.img, cv2.CV_64F).var()
        if laplacian < 100:
            kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
            roi = cv2.filter2D(roi, -1, kernel)
        # return cropped image
        return roi
    