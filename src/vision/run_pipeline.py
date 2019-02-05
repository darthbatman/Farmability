from hslpipline import *
import sys
import cv2

filename = "../assets/fields/generated_fields/field0.png"
h = 24
s = 17
l = 41

# python3 run_pipeline.py ../assets/fields/generated_fields/field0.jpg 24 17 41
if(len(sys.argv) == 2):
    filename = sys.argv[1]

if(len(sys.argv) >= 5):
    filename = sys.argv[1]
    h = float(sys.argv[2])
    s = float(sys.argv[3])
    l = float(sys.argv[4])

image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
cv2.namedWindow("Image")

pipeline = HSLPipline(h, s, l, filename)
processed_image = pipeline.process(image)

processed_filename = filename.split('.')[0] + "_processed.png"
cv2.imshow("Image", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
