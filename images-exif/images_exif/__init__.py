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
    return


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('ramses')
    return config.make_wsgi_app()
