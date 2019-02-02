from PIL import Image
from google_maps_static_api_request import GoogleMapsStaticAPIRequest


def crop_out_google_footer(source_image_path, cropped_image_path):
    Image.open(source_image_path).convert('RGB').save(source_image_path)
    image_obj = Image.open(source_image_path)
    crop_end_x = image_obj.size[0]
    crop_end_y = image_obj.size[1] - 30
    cropped_image = image_obj.crop((0, 0, crop_end_x, crop_end_y))
    cropped_image.save(cropped_image_path)


def save_image_for_location(image_path, latitude, longitude):
    request = GoogleMapsStaticAPIRequest(
        'satellite',
        (latitude, longitude),
        15,
        (600, 300))
    request.save_image(image_path)
    crop_out_google_footer(image_path, image_path)


def save_image_for_google_maps_url(image_path, google_maps_url):
    latitude = google_maps_url.split('@')[1].split(',')[0]
    longitude = google_maps_url.split('@')[1].split(',')[1]
    save_image_for_location(image_path, latitude, longitude)
