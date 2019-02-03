from hslpipline import *
import sys
import cv2
import time

filename = "test1.png"
h = 15
s = 20
l = 30

# python3 run_pipeline.py ../assets/fields/generated_fields/field0.jpg 24 17 41

if(len(sys.argv) >= 5):
    filename = sys.argv[1]
    h = float(sys.argv[2])
    s = float(sys.argv[3])
    l = float(sys.argv[4])

image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
cv2.namedWindow("Image")

pipeline = HSLPipline(h, s, l)
processed_image = pipeline.process(image)

processed_filename = filename.split('.')[0] + "_processed.png"
cv2.imwrite(processed_filename, image)
cv2.imshow("Image", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
