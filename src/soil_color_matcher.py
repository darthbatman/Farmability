import sys
import soil_color

if __name__ == '__main__':
    soil_match = soil_color.find_closest_soil_match_by_color(
        (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])),
        '../data/soil.json')
    print(soil_match)
