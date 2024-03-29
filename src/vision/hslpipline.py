import cv2
import numpy
import math
from enum import Enum


class HSLPipline:
    """
    An OpenCV pipeline generated by GRIP.
    """

    filename = ""

    def __init__(self, h, s, l, filename):
        """initializes all values to presets or None if need to be set
        """
        self.__blur_0_type = BlurType.Box_Blur
        self.__blur_0_radius = 0.0

        self.blur_0_output = None

        self.hue_threshold_range = 5.0
        self.sat_threshold_range = 100.0
        self.lum_threshold_range = 100.0
        HSLPipline.filename = filename

        self.__rgb_threshold_input = self.blur_0_output
        self.__rgb_threshold_red = [74.89415879631667, 127.99960815047024]
        self.__rgb_threshold_green = [0.0, 207.47727272727275]
        self.__rgb_threshold_blue = [41.82286785379568, 109.53409090909093]

        self.rgb_threshold_output = None

        self.__hsl_threshold_input = self.blur_0_output

        low = h - self.hue_threshold_range
        if low < 0:
            low += 180
        hi = h + self.hue_threshold_range
        if hi > 180:
            hi %= 180
        self.__hsl_threshold_hue = [low, hi]
        self.__hsl_threshold_saturation = [max(0, s - self.sat_threshold_range), min(254.0, s + self.sat_threshold_range)]
        self.__hsl_threshold_luminance = [max(0, l - self.lum_threshold_range), min(254.0, l + self.lum_threshold_range)]
        self.hsl_threshold_output = None

        self.__blur_1_input = self.hsl_threshold_output
        self.__blur_1_type = BlurType.Median_Filter
        self.__blur_1_radius = 8.5

        self.blur_1_output = None

        self.__find_contours_input = self.blur_1_output
        self.__find_contours_external_only = False

        self.find_contours_output = None

    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Blur0:
        self.__blur_0_input = source0
        print(source0)
        (self.blur_0_output) = self.__blur(
            self.__blur_0_input, self.__blur_0_type, self.__blur_0_radius)

        # Step RGB_Threshold0:
        self.__rgb_threshold_input = self.blur_0_output
        (self.rgb_threshold_output) = self.__rgb_threshold(self.__rgb_threshold_input,
                                                           self.__rgb_threshold_red, self.__rgb_threshold_green, self.__rgb_threshold_blue)

        # Step HSL_Threshold0:
        self.__hsl_threshold_input = self.blur_0_output
        (self.hsl_threshold_output) = self.__hsl_threshold(self.__hsl_threshold_input,
                                                           self.__hsl_threshold_hue, self.__hsl_threshold_saturation, self.__hsl_threshold_luminance)

        # Step Blur1:
        self.__blur_1_input = self.hsl_threshold_output
        (self.blur_1_output) = self.__blur(
            self.__blur_1_input, self.__blur_1_type, self.__blur_1_radius)

        # Step Find_Contours0:
        self.__find_contours_input = self.blur_1_output
        (self.find_contours_output) = self.__find_contours(
            self.__find_contours_input, self.__find_contours_external_only, source0)

        return self.find_contours_output[1]

    @staticmethod
    def __rgb_threshold(input, red, green, blue):
        """Segment an image based on color ranges.
        Args:
            input: A BGR numpy.ndarray.
            red: A list of two numbers the are the min and max red.
            green: A list of two numbers the are the min and max green.
            blue: A list of two numbers the are the min and max blue.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        return cv2.inRange(out, (red[0], green[0], blue[0]),  (red[1], green[1], blue[1]))

    @staticmethod
    def __hsl_threshold(input, hue, sat, lum):
        """Segment an image based on hue, saturation, and luminance ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max luminance.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HLS)
        return cv2.inRange(out, (hue[0], lum[0], sat[0]),  (hue[1], lum[1], sat[1]))

    @staticmethod
    def __blur(src, type, radius):
        """Softens an image using one of several filters.
        Args:
            src: The source mat (numpy.ndarray).
            type: The blurType to perform represented as an int.
            radius: The radius for the blur as a float.
        Returns:
            A numpy.ndarray that has been blurred.
        """
        if(type is BlurType.Box_Blur):
            ksize = int(2 * round(radius) + 1)
            print(src)
            print(ksize)
            return cv2.blur(src, (ksize, ksize))
        elif(type is BlurType.Gaussian_Blur):
            ksize = int(6 * round(radius) + 1)
            return cv2.GaussianBlur(src, (ksize, ksize), round(radius))
        elif(type is BlurType.Median_Filter):
            ksize = int(2 * round(radius) + 1)
            return cv2.medianBlur(src, ksize)
        else:
            return cv2.bilateralFilter(src, -1, round(radius), round(radius))

    @staticmethod
    def __find_contours(input, external_only, source0):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST

        method = cv2.CHAIN_APPROX_SIMPLE
        contours = cv2.findContours(input, mode, method)

        for contour in contours:  # Trust me, need the useless for loop
            for i in range(0, len(contour)):
                cv2.drawContours(source0, contour, i, (numpy.random.randint(255), numpy.random.randint(255), numpy.random.randint(255)), 3)
            break

        processed_filename = HSLPipline.filename.split('.')[0] + "_processed.png"
        cv2.imwrite(processed_filename, source0)

        return contours, source0


BlurType = Enum(
    'BlurType', 'Box_Blur Gaussian_Blur Median_Filter Bilateral_Filter')
