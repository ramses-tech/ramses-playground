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
def fill_exif(event):
    # Test image: http://bit.ly/1VTFA5W
    url = event.fields['url'].new_value
    response = requests.get(url)
    image_file = StringIO(response.content)
    raw_exif = exifread.process_file(image_file, details=False)
    exclude = ('Thumbnail', 'Interoperability', 'MakerNote')
    exif = {key: val.values for key, val in raw_exif.items()
            if key.split()[0] not in exclude}


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()
