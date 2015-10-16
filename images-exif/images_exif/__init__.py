from StringIO import StringIO

import exifread
import requests
from pyramid.config import Configurator
from ramses import registry


@registry.add
def validate_url_present(event):
    if 'url' not in event.fields or not event.fields['url'].new_value:
        raise KeyError('Missing required field: "url"')


@registry.add
def populate_name(event):
    if 'name' not in event.fields:
        url = event.fields['url'].new_value
        full_name = url.strip().split('/')[-1]
        name = full_name.split('.')[0]
        event.set_field_value('name', name)


@registry.add
def readonly_url(event):
    if event.view.request.action != 'create' and 'url' in event.fields:
        raise Exception('Field "url" can not be changed')


@registry.add
def populate_exif(event):
    # Test image: http://bit.ly/1VTFA5W
    url = event.fields['url'].new_value
    response = requests.get(url)
    image_file = StringIO(response.content)
    raw_exif = exifread.process_file(image_file, details=False)

    # EXIF data
    exclude = ('Thumbnail', 'Interoperability', 'MakerNote', 'GPS')
    exif_data = {key: val.printable for key, val in raw_exif.items()
                 if key.split()[0] not in exclude}
    event.set_field_value('exif', exif_data)
    # GPS data
    gps_data = {key.split()[-1]: val.values
                for key, val in raw_exif.items()
                if key.startswith('GPS')}

    lat, lon = get_lat_lon(gps_data)
    event.set_field_value('location', {'lat': lat, 'lon': lon})


# Customized versions of https://gist.github.com/erans/983821
def _to_degrees(value):
    deg = value[0]
    deg = float(deg.num) / float(deg.den)

    minute = value[1]
    minute = float(minute.num) / float(minute.den)

    sec = value[2]
    sec = float(sec.num) / float(sec.den)

    return deg + (minute / 60.0) + (sec / 3600.0)


def get_lat_lon(geo_data):
    lat = None
    lon = None

    try:
        gps_lat = geo_data['GPSLatitude']
        gps_lat_ref = geo_data.get('GPSLatitudeRef', 'N')
        gps_lon = geo_data['GPSLongitude']
        gps_lon_ref = geo_data.get('GPSLongitudeRef', 'E')

        if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
            lat = _to_degrees(gps_lat)
            if gps_lat_ref.upper() != 'N':
                lat = 0 - lat

            lon = _to_degrees(gps_lon)
            if gps_lon_ref.upper() != 'E':
                lon = 0 - lon
    except (KeyError, IndexError):
        pass

    return lat, lon


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()
