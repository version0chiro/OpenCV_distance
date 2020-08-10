from imutils import paths
import numpy as np
import imutils
import cv2


def find_marker(image):
    # convert the image to grayscale,blur it and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 10, 110)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image;

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    return cv2.minAreaRect(c)

# We are making the assumption that the contour with the largest area is our piece of paper.
# This assumption works for
# this particular example, but in reality finding the marker in an image is highly application specific.

def distance_to_camera(knownWidth, focalLength, perWidht):
    return (knownWidth * focalLength) / perWidht


# initialize the known distance from the camera to the object, which
# in this case is 24 inches

KNOWN_DISTANCE = 19.685  # replace with your distance

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide

KNOWN_WIDTH = 4.85 # replace with your width

# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread("images/2ft.png")
scale_percent = 20

#calculate the 50 percent of original dimensions
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)

x1 = cv2.resize(image,dsize)

marker = find_marker(x1)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# loop over the images
for imagePath in sorted(paths.list_images("images")):
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    image = cv2.resize(image, dsize)
    marker = find_marker(image)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    # draw a bounding box around the image and display it
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    box = np.int0(box)
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fft" % (inches * 2.54),
                (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
    print(str(inches*2.54))

    cv2.imshow("image", image)
    cv2.waitKey(0)
