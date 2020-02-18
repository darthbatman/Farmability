from PIL import Image
from lib import google_maps_static_api_request


def crop_out_google_footer(source_image_path, cropped_image_path):
    Image.open(source_image_path).convert('RGB').save(source_image_path)
    image_obj = Image.open(source_image_path)
    crop_end_x = image_obj.size[0]
    crop_end_y = image_obj.size[1] - 30
    cropped_image = image_obj.crop((0, 0, crop_end_x, crop_end_y))
    cropped_image.save(cropped_image_path)


def save_image_for_location(image_path, zoom, coordinates):
    request = google_maps_static_api_request.GoogleMapsStaticAPIRequest(
        'satellite',
        (coordinates[0], coordinates[1]),
        zoom,
        (600, 600))
    request.save_image(image_path)
    crop_out_google_footer(image_path, image_path)


def save_image_for_google_maps_url(image_path, google_maps_url):
    print(image_path)
    latitude = google_maps_url.split('@')[1].split(',')[0]
    longitude = google_maps_url.split('@')[1].split(',')[1]
    zoom = 16
    if 'z' in google_maps_url:
        zoom_str = google_maps_url.split('@')[1].split(',')[2].split('z')[0]
        zoom = int(float(zoom_str))
    elif 'm' in google_maps_url:
        meters_str = google_maps_url.split('@')[1].split(',')[2].split('m')[0]
        meters = int(meters_str)
        if meters < 500:
            zoom = 17
        elif meters < 1000:
            zoom = 16
        elif meters < 1500:
            zoom = 15
        else:
            zoom = 14
    save_image_for_location(image_path, zoom, (latitude, longitude))
