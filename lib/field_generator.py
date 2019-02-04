import sys
import map_to_image


if __name__ == '__main__':
    map_to_image.save_image_for_google_maps_url(sys.argv[1], sys.argv[2])
