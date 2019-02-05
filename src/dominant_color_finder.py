import sys
import dominant_image_color

if __name__ == '__main__':
    most_dominant_color = dominant_image_color.dominant_color(
        sys.argv[1])
    print(most_dominant_color)
