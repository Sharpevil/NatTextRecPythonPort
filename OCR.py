import cv2
import numpy as np

image_file = "./Lady Deborah.png"

image = cv2.imread(image_file)
mser = cv2.MSER_create()
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hull_image = image.copy()
rect_image = image.copy()
rot_rect_image = image.copy()

MAX_ASPECT_RATIO = 2

# Returns False if a box exceeds the MAX_ASPECT_RATIO in either dimension. Otherwise returns true.
def fits_ratio(width, height):
    if width/height <= MAX_ASPECT_RATIO and height/width <= MAX_ASPECT_RATIO:
        return True
    else:
        return False


# detectRegions returns more information than we require, so the second value is thrown away.
regions, _ = mser.detectRegions(grey)

for region in regions:
    min_x = 999999
    min_y = 999999
    max_x = -1
    max_y = -1

    for pair in region:
        if pair[0] < min_x:
            min_x = pair[0]
        elif pair[0] > max_x:
            max_x = pair[0]
        if pair[1] < min_y:
            min_y = pair[1]
        elif pair[1] > max_y:
            max_y = pair[1]

    if fits_ratio(max_x - min_x, max_y - min_y):

        cv2.rectangle(rect_image, (max_x, min_y), (min_x, max_y), (0, 255, 0), 2)

        rect = cv2.minAreaRect(region)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(rot_rect_image, [box], 0, (0, 0, 255), 2)

hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
cv2.polylines(hull_image, hulls, 1, (0, 0, 255), 2)
cv2.imshow('image', hull_image)
cv2.waitKey(0)
cv2.imshow('image', rect_image)
cv2.waitKey(0)
cv2.imshow('image', rot_rect_image)
cv2.waitKey(0)
cv2.imwrite("./Grey_image.png", hull_image)


