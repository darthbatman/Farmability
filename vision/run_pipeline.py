from hslpipline import *
import sys
import cv2
import time

filename = "test1.png"

if(len(sys.argv) > 1):
    filename = sys.argv[0]

image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
cv2.namedWindow("Image")

pipeline = HSLPipline()
processed_image = pipeline.process(image)

processed_filename = filename.split('.')[0] + "_processed.png"
cv2.imwrite(processed_filename, image)
cv2.imshow("Image", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
