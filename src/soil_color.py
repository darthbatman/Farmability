import json
import colorsys


def find_closest_soil_match_by_color(color, soil_data_file_path):
    soil_color_hls = colorsys.rgb_to_hls(color[0], color[1], color[2])
    with open(soil_data_file_path) as soil_data_file:
        soil_data = json.load(soil_data_file)
    soil_types = soil_data['soil_types']
    hue_min_diff = 1
    closest_soil = ''
    for i in range(0, len(soil_types)):
        soil_color = soil_types[i]['color']
        hls_color = colorsys.rgb_to_hls(
            int(soil_color['r']),
            int(soil_color['g']),
            int(soil_color['b']))
        if abs(soil_color_hls[0] - hls_color[0]) < hue_min_diff:
            hue_min_diff = abs(soil_color_hls[0] - hls_color[0])
            closest_soil = soil_types[i]
    return closest_soil